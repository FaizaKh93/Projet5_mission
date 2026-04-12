---
title: ML Prediction API with FastAPI and Automated Testing
emoji: 🚀
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# Auteur

Faiza Khelladi  
Formation Data Scientist – Machine Learning
Mission du projet5 : Déployez un modèle de Machine Learning

------------------------------------------------------------------
# ML Prediction API – Employee Attrition Prediction

## 1. Objectif du projet

Ce projet vise à prédire le risque de départ (attrition) des employés dans une ESN à l’aide d’un modèle de Machine Learning exposé via une API FastAPI.

L’objectif est d’aider les équipes RH à :

- anticiper les départs des employés
- comprendre les facteurs expliquant l’attrition
- mettre en place des actions pour réduire le turnover et préserver les talents

------------------------------------------------------------------

## 2. Contexte

L’entreprise souhaite anticiper les départs des employés à l’aide d’un modèle de Machine Learning.

------------------------------------------------------------------

## 3. Données

Les données proviennent de sources RH (SIRH, évaluations, sondages) et ont été prétraitées en amont (nettoyage, feature engineering, encodage) dans le projet 4 afin de produire un dataset CSV directement exploitable par le modèle ; l’API consomme uniquement ces données déjà prétraitées.

------------------------------------------------------------------

## 4. Modélisation

Le modèle utilisé est un **XGBoost** sélectionné pour ses performances.

### 4.1 Performance du modèle 

- Modèle : XGBoost
- Score F2 : 0.613
- Seuil optimal : 0.711

------------------------------------------------------------------

## 5. Structure du projet

```
├── app.py # API FastAPI (point d’entrée)
├── database/ # Configuration DB + modèles SQLAlchemy
├── models/ # Modèle ML entraîné
├── data/ # Données prétraitées (CSV)
├── functions/ # Fonctions métier / preprocessing
├── tests/ # Tests unitaires et fonctionnels (Pytest)
├── notebooks/ # Analyse exploratoire (EDA)
├── presentation/ # Support de présentation
├── .github/workflows/ # Pipeline CI/CD (GitHub Actions)
├── Dockerfile # Conteneurisation
├── pyproject.toml # Dépendances du projet
├── README.md # Documentation principale
└── .gitignore
```

------------------------------------------------------------------
## 6. Utilisation de l’API

### 6.1 Accès à l’API

L’API est déployée et accessible via :

https://faiza93-ml-prediction-api.hf.space

------------------------------------------------------------------
### 6.2 Documentation interactive (Swagger)

Vous pouvez tester les endpoints directement ici :

https://faiza93-ml-prediction-api.hf.space/docs

------------------------------------------------------------------
### 6.3 Endpoint principal

**POST /predict**

Permet de prédire le risque de départ des employés. 

------------------------------------------------------------------
### 6.4 Exemple de requête

```json
{
  "rows": [
    [41, 5993, 0, 8, 0, 6, 0, 4, 0, 2, 0, 3, 0, 4, 1, 1, 0, 11, 0, 0, 0, 1, 0, 2, 1, 0, 0, 0, 0, 2, 0, 0, 0.2857, 1, 6924.27]
  ]
}
```
------------------------------------------------------------------
### 6.5 Exemple de réponse
```json
{
  "predictions": [1]
}
```
------------------------------------------------------------------
### 6.6 Interprétation
0 -> employé reste
1 -> employé quitte l'entreprise

------------------------------------------------------------------
## 7. Déploiement et CI/CD

Le projet est déployé sur **Hugging Face Spaces** avec **Docker**.

### 7.1 Déploiement

- API publique : [https://faiza93-ml-prediction-api.hf.space](https://faiza93-ml-prediction-api.hf.space)
- Documentation Swagger : [https://faiza93-ml-prediction-api.hf.space/docs](https://faiza93-ml-prediction-api.hf.space/docs)

Le conteneur est défini dans le fichier `Dockerfile` et lancé automatiquement par Hugging Face Spaces.

------------------------------------------------------------------
### 7.2 Pipeline CI/CD

Le projet utilise **GitHub Actions** pour automatiser :

- l’exécution des tests
- la validation du code
- le déploiement automatique vers Hugging Face Spaces

Deux workflows principaux sont utilisés :

- `ci.yml` : exécute les tests Pytest à chaque push / pull request
- `hf-deploy.yml` : synchronise le dépôt vers Hugging Face lors d’un push sur `main`

------------------------------------------------------------------
### 7.3 Gestion des environnements

Le projet distingue plusieurs environnements :

- **Local** : développement et tests manuels
- **CI** : exécution automatisée des tests avec mock de la base
- **Production** : API déployée sur Hugging Face avec PostgreSQL distant

------------------------------------------------------------------
### 7.4 Gestion des secrets

Les secrets ne sont pas stockés dans le code source.

- `HF_TOKEN` est stocké dans les GitHub Secrets pour le déploiement
- `DATABASE_URL` est stocké dans les Secrets du Space Hugging Face pour la connexion à PostgreSQL

------------------------------------------------------------------
## 8. Tests

Le projet inclut des tests unitaires et fonctionnels réalisés avec **Pytest**.

------------------------------------------------------------------
### 8.1 Types de tests

- Tests des fonctions métier
- Tests de l’API (endpoints FastAPI)
- Tests de performance du modèle
- Tests de chargement du modèle
- Tests de chargement des données

Les tests permettent de valider :

- le bon fonctionnement de l’API
- la gestion des cas limites (valeurs invalides, NaN, etc.)
- la stabilité du modèle

------------------------------------------------------------------
### 8.2 Exécution des tests

```bash
pytest tests/
```
------------------------------------------------------------------
## 9. Base de données

Les prédictions sont stockées dans une base **PostgreSQL** hébergée sur Render.

------------------------------------------------------------------
### 9.1 Modèle de données

Une table `predictions` est utilisée pour enregistrer :

- `id` : identifiant unique  
- `input_data` : données envoyées au modèle (JSON)  
- `prediction` : résultat de la prédiction  
- `created_at` : date de création  

---------------------------------------------------------------------
### 9.2 Fonctionnement

À chaque appel de l’endpoint `/predict` :

1. les données sont envoyées au modèle  
2. une prédiction est générée  
3. les données et la prédiction sont enregistrées en base  

------------------------------------------------------------------
### 9.3 Vérification du fonctionnement

La persistance des données a été validée en connectant un client PostgreSQL (pgAdmin) à la base distante.

------------------------------------------------------------------
## 10. Installation locale

### 10.1 Prérequis

- Python 3.10+
- uv (gestionnaire de dépendances) 

------------------------------------------------------------------
### 10.2 Installation
- cloner le dépôt

```bash
git clone https://github.com/FaizaKh93/Projet5_mission.git
cd Projet5_mission
```
- Installer les dépendances 
```bash
uv sync 
```
------------------------------------------------------------------
### 10.3 Lancer l'API
```bash
uv run uvicorn app:app --reload
```

------------------------------------------------------------------
### 10.4 Accès local
API : http://127.0.0.1:8000
Documentation Swagger : http://127.0.0.1:8000/docs

------------------------------------------------------------------
## 11. Choix techniques

### 11.1 FastAPI

FastAPI a été choisi pour développer l’API car il permet de créer rapidement des endpoints performants tout en générant automatiquement une documentation interactive (Swagger).

Il facilite également la validation des données en entrée grâce à Pydantic, ce qui permet de sécuriser l’API et de gérer les erreurs (types incorrects, valeurs manquantes, etc.).

---
------------------------------------------------------------------

## 11. Choix techniques

------------------------------------------------------------------

## 11. Choix techniques

### 11.1 FastAPI
FastAPI permet de créer une API performante avec validation automatique des données (Pydantic) et documentation interactive (Swagger).  
Il facilite le développement rapide tout en garantissant la robustesse des entrées utilisateur.

---

### 11.2 XGBoost
XGBoost est un modèle performant pour les données tabulaires, capable de capturer des relations complexes entre variables.  
Il a été retenu car il offre les meilleures performances (score F2) sur ce problème d’attrition.

---

### 11.3 PostgreSQL (Render) 
PostgreSQL est utilisé pour stocker les prédictions de manière persistante et structurée.  
La base est hébergée sur Render, ce qui permet une gestion simple et accessible en production.

---

### 11.4 Docker & Hugging Face Spaces
Docker permet de containeriser l’application pour garantir un environnement reproductible.  
Le déploiement est réalisé sur Hugging Face Spaces, facilitant l’hébergement et l’exposition de l’API.

---

### 11.5 GitHub Actions (CI/CD)
GitHub Actions automatise les tests, la validation du code et le déploiement.  
Il permet de synchroniser automatiquement le dépôt avec Hugging Face à chaque mise à jour.