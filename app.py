import joblib

import pandas as pd
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel # définir et valider la structure des données entrantes

from sqlalchemy.orm import Session

from database.db_config import get_db, Base, engine
from database.create_db import Prediction

#===============================================================
#===============================================================
#===============================================================

# Initialisation de l'app
app = FastAPI()

# Création automatique des tables au démarrage de l'application (test distant)  
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

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

    for row, pred in zip(data.rows, preds):
        db_record = Prediction(
            input_data=row,
            n_features=len(reference_columns),
            prediction=float(pred)
        )
        db.add(db_record)

    db.commit()

    return {"predictions": preds.tolist()} 

