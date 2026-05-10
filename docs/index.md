# Documentation du projet

Bienvenue dans la documentation du projet **ML Prediction API**.

---

## Objectif

Cette API permet de prédire le risque d’attrition des employés à l’aide d’un modèle de Machine Learning.

---

## Architecture

Le projet repose sur les composants suivants :

- API développée avec FastAPI  
- Modèle XGBoost pour la prédiction  
- Base PostgreSQL (Render) pour stocker les résultats  
- Déploiement via Docker sur Hugging Face Spaces  
- Pipeline CI/CD avec GitHub Actions  

---

## Utilisation rapide

Accéder à l’API :

https://faiza93-ml-prediction-api.hf.space

Documentation interactive :

https://faiza93-ml-prediction-api.hf.space/docs

---

## Endpoint principal

POST `/predict`

Permet de prédire le risque d’attrition des employés.

---

## Exemple de requête

```json
{
  "rows": [
    [41, 5993, 0, 8, 0, 6, 0, 4, 0, 2, 0, 3, 0, 4, 1, 1, 0, 11, 0, 0, 0, 1, 0, 2, 1, 0, 0, 0, 0, 2, 0, 0, 0.2857, 1, 6924.27]
  ]
}
```
---

##  Exemple de réponse
```json
{
  "predictions": [1]
}
```

---

## Interprétation

0 -> employé reste
1 -> employé quitte l'entreprise

---

## Base de données 

Les prédictions sont stockées dans une base PostgreSQL sur Render, permettant de tracer les résultats et analyser l’utilisation de l’API.