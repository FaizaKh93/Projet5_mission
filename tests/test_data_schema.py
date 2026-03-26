import os
import pandas as pd

X_PATH = "data/processed/X_encoded.csv"
Y_PATH = "data/processed/y.csv"


def test_encoded_data_file_exists():
    assert os.path.exists(X_PATH), f"Fichier introuvable : {X_PATH}"


def test_target_file_exists():
    assert os.path.exists(Y_PATH), f"Fichier introuvable : {Y_PATH}"


def test_encoded_data_can_be_loaded():
    X = pd.read_csv(X_PATH)
    assert X is not None
    assert not X.empty


def test_target_can_be_loaded():
    y = pd.read_csv(Y_PATH)
    assert y is not None
    assert not y.empty