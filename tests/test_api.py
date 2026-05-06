import os
import numpy as np
# Permet de simuler des requêtes HTTP (GET, POST) vers l’API sans lancer un serveur réel
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

# importer l'application FastAPI
from app import app, get_db 
#from db_config import get_db


# créer un client de test basé sur l’application
client = TestClient(app)

HEADERS = {"x-api-key": "test_key"}
os.environ["API_KEY"] = "test_key"
# ================================
# Test de la route racine "/"
# ================================
def test_root():
    # envoi d'une requête GET sur "/"
    response = client.get("/")

    # Vérifier que la réponse HTTP est OK (200)
    assert response.status_code == 200

    # Vérifier que le contenu retourné est celui attendu
    assert response.json() == {"message": "API OK"}


# ================================
# Test de l’endpoint "/health"
# ================================
def test_health():
    response = client.get("/health")

    # Vérifier que la requête fonctionne
    assert response.status_code == 200

    # récupèrer le contenu JSON
    data = response.json()

    # Vérifier la présence des clés importantes
    assert "status" in data
    assert data["status"] == "ok"

    # Vérifier que le modèle est chargé
    assert "model_loaded" in data

    # Vérifier que le nombre de features est présent
    assert "n_features" in data


# ================================
# Test de l’endpoint "/columns"
# ================================
def test_columns():
    response = client.get("/columns")

    assert response.status_code == 200

    data = response.json()

    # Vérifier que la clé "columns" existe
    assert "columns" in data

    # Vérifier que c’est bien une liste
    assert isinstance(data["columns"], list)

    # Vérifier qu’il y a au moins une colonne
    assert len(data["columns"]) > 0


# ================================
# Test de l’endpoint "/sample"
# ================================
def test_sample():
    # simuler la variable d’environnement
    import os
    os.environ["API_KEY"] = "test_key"
    #headers = {"x-api-key": "test_key"}

    response = client.get("/sample", headers=HEADERS)

    assert response.status_code == 200

    data = response.json()

    # Vérifier que les données sont présentes
    assert "rows" in data

    # Vérifier que c’est une liste
    assert isinstance(data["rows"], list)

    # Vérifier qu’il y a au moins une ligne
    assert len(data["rows"]) > 0


# ================================
# Test de prédiction avec input valide -- fake DB
# ================================
def test_predict_valid_input():
    # simuler la variable d’environnement
    import os
    os.environ["API_KEY"] = "test_key"
    #headers = {"x-api-key": "test_key"}

    # créer une fausse db
    fake_db = MagicMock()
    
    # remplacer temporairement get_db
    def override_get_db():
        yield fake_db

    # instruction à FastAPI afin d’utiliser la fausse base dans ce test
    app.dependency_overrides[get_db] = override_get_db

    try:
        sample_response = client.get("/sample", headers=HEADERS)
        sample_data = sample_response.json()

        payload = {
            "rows": sample_data["rows"][:2]
        }

        response = client.post("/predict", json=payload,headers=HEADERS)
        
        # Vérifier que la requête fonctionne
        assert response.status_code == 200

        response_json = response.json()

        # Vérifier que les prédictions sont présentes
        assert "predictions" in response_json
        assert len(response_json["predictions"]) == 2
        
        # vérifier que le code a bien tenté d’ajouter en base
        assert fake_db.add.called

        # vérifier que le code a bien tenté de sauvegarder
        assert fake_db.commit.called

    finally:
        app.dependency_overrides.clear()

# ================================
# Test de prédiction avec input valide -- real DB
# ================================
""" def test_predict_valid_input(): 
    # récupèrer un exemple valide via l’API
    sample_response = client.get("/sample")
    sample_data = sample_response.json()

    # prendre seulement 2 lignes pour le test
    payload = {
        "rows": sample_data["rows"][:2]
    }

    # envoi d'une requête POST sur /predict
    response = client.post("/predict", json=payload)

    # Vérifier que la requête fonctionne
    assert response.status_code == 200

    data = response.json()

    # Vérifier que les prédictions sont présentes
    assert "predictions" in data

    # Vérifier que c’est une liste
    assert isinstance(data["predictions"], list)

    # Vérifier que le nombre de prédictions correspond au nombre d’inputs
    assert len(data["predictions"]) == len(payload["rows"]) """


# ================================
# Test : input vide (erreur)
# ================================
def test_predict_empty_input():
    # simuler la variable d’environnement
    import os
    os.environ["API_KEY"] = "test_key"
    #headers = {"x-api-key": "test_key"}

    payload = {
        "rows": []
    }

    response = client.post("/predict", json=payload, headers=HEADERS)

    # On attend une erreur 400 (Bad Request)
    assert response.status_code == 400

    # Vérifier le message d’erreur
    assert response.json()["detail"] == "Input data for prediction is empty."


# ================================
# Test : lignes de tailles différentes (erreur)
# ================================
def test_predict_inconsistent_row_lengths():
    # simuler la variable d’environnement
    import os
    os.environ["API_KEY"] = "test_key"
    #headers = {"x-api-key": "test_key"}

    payload = {
        "rows": [
            [1.0, 2.0, 3.0],
            [1.0, 2.0]  # ligne plus courte → erreur attendue
        ]
    }

    response = client.post("/predict", json=payload, headers=HEADERS)

    assert response.status_code == 400

    # Vérifier le message d’erreur attendu 
    assert response.json()["detail"] == "All rows must have the same number of values."


# ================================
# Test : mauvais nombre de features (erreur)
# ================================
def test_predict_wrong_number_of_features():
    # simuler la variable d’environnement
    import os
    os.environ["API_KEY"] = "test_key"
    #headers = {"x-api-key": "test_key"}

    payload = {
        "rows": [
            [1.0, 2.0, 3.0]  # nombre de colonnes incorrect
        ]
    }

    response = client.post("/predict", json=payload, headers=HEADERS)

    assert response.status_code == 400

    # Vérifier que le message contient l’erreur attendue
    detail = response.json()["detail"]
    assert "Wrong number of features." in detail

# ================================
# Test : mauvais types de features : string, booleéen, dict., NaN
# ================================
def test_predict_invalid_types():
    # simuler la variable d’environnement
    import os
    os.environ["API_KEY"] = "test_key"
    #headers = {"x-api-key": "test_key"}

    invalid_payloads = [
        {"rows": [["a", "b", "c"]]}, 
        {"rows": [[1.0, "a", 3.0]]},
        #{"rows": [[True, False, True]]},
        {"rows": [[{"a": 1}, {"b": 2}]]},
        #{"rows": [[1.0, None, 3.0]]}, 
        #{"rows": [[1.0, np.nan, 3.0]]},      
    ]

    for payload in invalid_payloads:
        response = client.post("/predict", json=payload, headers=HEADERS)
        assert response.status_code == 422

def test_predict_null_values():
    # simuler la variable d’environnement
    import os
    os.environ["API_KEY"] = "test_key"
    #headers = {"x-api-key": "test_key"}

    payload = {
        "rows": [
            [1.0, None, 3.0]
        ]
    }

    response = client.post("/predict", json=payload, headers=HEADERS)
    assert response.status_code in [400, 422]