import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel  # définir et valider la structure des données entrantes

from sqlalchemy.orm import Session

from database.db_config import get_db
from database.create_db import Prediction, InputDataDB, ModelVersion

#===============================================================
#===============================================================
#===============================================================

# Initialisation de l'app
app = FastAPI()

# Charger le modèle et les données
MODEL_PATH = "models/trained_model.pkl"
DATA_PATH = "data/processed/X_encoded.csv"

model = joblib.load(MODEL_PATH) 
reference_columns = pd.read_csv(DATA_PATH, nrows=0).columns.tolist()

class InputData(BaseModel):
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
# endpoint columns : get data to feed /predict
#===============================================================
@app.get("/sample")
def sample():
    X_sample = pd.read_csv(DATA_PATH, nrows=5)
    return {"rows": X_sample.values.tolist()}

#===============================================================
# endpoint predict
#===============================================================
@app.post("/predict")
def predict(data: InputData, db: Session = Depends(get_db)):
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
    # case 2 : wrong number of columns
    #======================================
    if received_n_features != expected_n_features:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Wrong number of features. "
                f"Expected {expected_n_features}, got {received_n_features}."
            )
        )
    #======================================
    # transformer en DataFrame
    X = pd.DataFrame(data.rows, columns=reference_columns)

    # prédictions
    preds = model.predict(X)

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
    for row, pred in zip(data.rows, preds):
        input_record = InputDataDB(
        input_data=row,
        n_features=len(reference_columns)
        )

        db.add(input_record)
        db.flush()

        prediction_record = Prediction(
        input_id=input_record.id,
        # lien vers la version du modèle utilisée
        model_version_id=model_version.id,
        # valeur prédite
        prediction=float(pred)
        )

        db.add(prediction_record)

    db.commit()

    return {"predictions": preds.tolist()}

