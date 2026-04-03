import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel # définir et valider la structure des données entrantes

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
# endpoints 
#===============================================================
# endpoint fast test
@app.get("/")
def root():
    return {"message": "API OK"}
#===============================================================
# endpoint health : status, loaded model, number of features
@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "n_features": len(reference_columns)
    }
#===============================================================
# endpoint columns : name of expected columns
@app.get("/columns")
def get_columns():
    return {"columns": reference_columns}
#===============================================================
# endpoint columns : get data to feed /predict
@app.get("/sample")
def sample():
    X_sample = pd.read_csv(DATA_PATH, nrows=2)
    return {"rows": X_sample.values.tolist()}
#===============================================================
# endpoint predict
@app.post("/predict")
def predict(data: InputData):
    # transformer en DataFrame
    X = pd.DataFrame(data.rows, columns=reference_columns)

    # prédictions
    preds = model.predict(X)

    return {"predictions": preds.tolist()}

