import joblib
import os
import pandas as pd

from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel  # définir et valider la structure des données entrantes

from sqlalchemy.orm import Session

from database.db_config import get_db, Base, engine
from database.create_db import Prediction, InputDataDB, ModelVersion, Employee

#===============================================================
#===============================================================
#===============================================================

# Initialisation de l'app
app = FastAPI()

# Récupération de la clé API depuis les variables d'environnement
API_KEY = os.getenv("API_KEY") 

# Vérification si la clé API envoyée par le client est correcte
def verify_api_key(x_api_key: str = Header(None)):
    expected_api_key = os.getenv("API_KEY") 
    # Si aucune clé API n'est définie côté serveur
    # => problème de configuration (ex : oubli dans HF Spaces)
    if not expected_api_key:
        raise HTTPException(
            status_code=500,  # erreur serveur
            detail="API key is not configured"
        )

    # Si la clé envoyée dans la requête (x-api-key) est différente de celle du serveur
    if x_api_key != expected_api_key:
        raise HTTPException(
            status_code=401,  # erreur d'authentification
            detail="Invalid or missing API key"
        )
    
# Création automatique des tables au démarrage de l'application (test distant)  
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Charger le modèle et les données
MODEL_PATH = "models/trained_model.pkl"
DATA_PATH = "data/processed/X_encoded.csv" 
SIRH_PATH = "data/extrait_sirh.csv"

model = joblib.load(MODEL_PATH) 
reference_columns = pd.read_csv(DATA_PATH, nrows=0).columns.tolist()

class InputData(BaseModel):
    employee_refs: list[int]
    rows: list[list[float]]
#===============================================================
#===============================================================
# endpoints 
#===============================================================
#=============================================================== 
# endpoint fast test
@app.get("/")
def root():
    return {"message": "API OK"}
#===============================================================
# endpoint health : status, loaded model, number of features
#===============================================================
@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "n_features": len(reference_columns)
    }

#===============================================================
# endpoint columns : name of expected columns
#===============================================================
@app.get("/columns")
def get_columns():
    return {"columns": reference_columns}

#===============================================================
# endpoint sample : get data to feed /predict
#===============================================================
@app.get("/sample")
def sample(api_key: str = Depends(verify_api_key)):
    X_sample = pd.read_csv(DATA_PATH, nrows=5)
    sirh_sample = pd.read_csv(SIRH_PATH, nrows=5)
    return {
        "employee_refs": sirh_sample["id_employee"].tolist(),
        "rows": X_sample.values.tolist()}

#===============================================================
# endpoint predict
#===============================================================
@app.post("/predict")
def predict(data: InputData, db: Session = Depends(get_db), api_key: str = Depends(verify_api_key)):
    #======================================
    # case 1 : empty input
    #======================================
    if not data.rows:
        raise HTTPException(
            status_code=400,
            detail="Input data for prediction is empty."
        )
    
    # length of each row  (number of columns)
    row_lengths = [len(row) for row in data.rows]

    # Number of features expected by the model
    expected_n_features = len(reference_columns)

    # Number of features received by the model
    received_n_features = row_lengths[0]

    #======================================
    # case 2 : check if rows have the same length
    #======================================
    # Vérifie que toutes les lignes ont la même longueur
    if len(set(row_lengths)) > 1:
        raise HTTPException(
            status_code=400,
            detail="All rows must have the same number of values."
        )

    #======================================
    # case 3 : wrong number of columns
    #======================================
    if received_n_features != expected_n_features:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Wrong number of features. "
                f"Expected {expected_n_features}, got {received_n_features}."
            )
        )
    
    # ================================ 
    # case 4 : null / NaN values
    # ================================
    for row in data.rows:
        for value in row:
            if pd.isna(value):
                raise HTTPException(
                    status_code=400,
                    detail="Invalid input: NaN or null values are not allowed."
                )
    #======================================
    # transformer en DataFrame
    X = pd.DataFrame(data.rows, columns=reference_columns)

    # prédictions
    preds = model.predict(X)

    #======================================
    # Récupérer les index des colonnes métier
    #======================================
    age_index = reference_columns.index("age")
    revenu_index = reference_columns.index("revenu_mensuel")
    #employee_index = reference_columns.index("revenu_mensuel")

    #======================================
    # Model Version
    #======================================
    # Vérifier si la version du modèle existe déjà en base
    model_version = (
        # interroger la table model_versions
        db.query(ModelVersion)
        .filter(
            # rechercher le modèle nommé XGBoost
            ModelVersion.model_name == "XGBoost",

            # rechercher spécifiquement la version v1
            ModelVersion.version == "v1"
        )
        # récupérer le premier résultat trouvé
        .first()
)
    # Si aucune version n'existe encore en base
    if model_version is None:
        # créer un nouvel enregistrement de version
        model_version = ModelVersion(
            model_name="XGBoost",
            version="v1"
        )

        # ajouter l'objet à la session SQLAlchemy
        db.add(model_version)

        # envoyer temporairement en base pour générer l'id
        db.flush()
 
    #======================================
    # InputDataDB & Prediction
    #======================================
    for employee_ref, row, pred in zip(data.employee_refs, data.rows, preds):
        #=======================================
        # Employee
        #=======================================
        # Vérifier si l'employé existe déjà
        employee = (
            db.query(Employee)
            .filter(Employee.employee_ref == str(employee_ref))
            .first()
        )

        # Si l'employé n'existe pas, le créer
        if employee is None:
            employee = Employee(
                employee_ref=str(employee_ref)
            )

            db.add(employee)
            db.flush()
        #=======================================  
        # inputs
        #=======================================
        input_record = InputDataDB(
        employee_id=employee.id,
        input_data=row,
        age=row[age_index],
        revenu=row[revenu_index],
        n_features=len(reference_columns)
        )

        db.add(input_record)
        db.flush()

        #=======================================
        # prediction
        #=======================================
        prediction_record = Prediction(
        input_id=input_record.id,
        employee_id=employee.id,
        # lien vers la version du modèle utilisée
        model_version_id=model_version.id,
        # valeur prédite
        prediction=float(pred)
        )

        db.add(prediction_record)

    db.commit()

    return {"predictions": preds.tolist()} 

