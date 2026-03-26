import os
import joblib
import pandas as pd

MODEL_PATH = "models/trained_model.pkl"
DATA_PATH = "data/processed/X_encoded.csv"


def test_model_file_exists():
    assert os.path.exists(MODEL_PATH), f"Fichier modèle introuvable : {MODEL_PATH}"


def test_model_can_be_loaded():
    model = joblib.load(MODEL_PATH)
    assert model is not None


def test_model_can_predict_on_encoded_data():
    model = joblib.load(MODEL_PATH)
    X = pd.read_csv(DATA_PATH)

    preds = model.predict(X.head(5))
    assert len(preds) == 5