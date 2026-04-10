import joblib
import pandas as pd
from sklearn.metrics import fbeta_score


MODEL_PATH = "models/trained_model.pkl"
X_PATH = "data/processed/X_encoded.csv"
Y_PATH = "data/processed/y.csv"


def test_model_f2_score_is_reasonable():
    model = joblib.load(MODEL_PATH)
    X = pd.read_csv(X_PATH)
    y = pd.read_csv(Y_PATH).squeeze()

    preds = model.predict(X)

    score = fbeta_score(y, preds, beta=2)

    assert score > 0.50 , f"F2 score too low: {score}"
    print(f"F2 score: {score}")