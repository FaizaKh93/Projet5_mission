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
### 6.7 Authentification et gestion des accès 
L’API implémente un mécanisme simple d’authentification basé sur une **clé API** afin de sécuriser les endpoints sensibles.

#### 6.7.1 Principe
 
Les endpoints suivants sont protégés :
- `/predict`
- `/sample`

Pour y accéder, il est nécessaire de fournir une clé API dans le header HTTP :

```http
x-api-key: votre_cle_api
```
La clé n’est pas fournie pour des raisons de sécurité.

Pour tester l’API, vous pouvez :
- contacter l’auteur afin d’obtenir une clé valide
- ou configurer votre propre variable d’environnement `API_KEY` dans les paramètres de Hugging Face Spaces.
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

La base repose sur quatre tables principales :

#### Table `employees`

Contient les informations de référence des employés.

Champs principaux :

- `id` : identifiant interne
- `employee_ref` : identifiant employé provenant du SIRH

---

#### Table `inputs`

Stocke les données envoyées au modèle avant prédiction.

Champs principaux :

- `id` : identifiant unique
- `employee_id` : référence vers l’employé
- `input_data` : données d’entrée au format JSON
- `age` : âge de l’employé
- `revenu` : revenu de l’employé
- `n_features` : nombre de variables utilisées
- `created_at` : date d’enregistrement

---

#### Table `predictions`

Contient les résultats des prédictions réalisées par le modèle.

Champs principaux :

- `id` : identifiant unique
- `input_id` : référence vers les données d’entrée
- `employee_id` : référence vers l’employé
- `model_version_id` : version du modèle utilisée
- `prediction` : résultat de la prédiction
- `created_at` : date de création

---

#### Table `model_versions`

Permet de tracer les versions du modèle déployé.

Champs principaux :

- `id` : identifiant unique
- `model_name` : nom du modèle
- `version` : version du modèle
- `created_at` : date de création

---

#### Relations entre les tables

- Un employé peut avoir plusieurs entrées (`employees` → `inputs`)
- Une entrée peut générer plusieurs prédictions (`inputs` → `predictions`)
- Chaque prédiction est associée à une version du modèle (`model_versions` → `predictions`)
- Chaque prédiction est liée à un employé pour assurer la traçabilité 

---------------------------------------------------------------------
### 9.2 Fonctionnement
À chaque appel de l’endpoint `/predict` :

1. les données d’entrée sont envoyées à l’API,
2. le modèle génère une prédiction,
3. les données sont enregistrées dans la table `inputs`,
4. l’employé associé est relié via `employee_id`,
5. la prédiction est enregistrée dans la table `predictions`,
6. la version du modèle utilisée est tracée via `model_versions`.

Ce mécanisme permet d’assurer une traçabilité complète des prédictions réalisées par le modèle.

------------------------------------------------------------------
### 9.3 Vérification du fonctionnement

La persistance des données a été validée en connectant des clients PostgreSQL
(pgAdmin et DBeaver) à la base distante hébergée sur Render.

Les vérifications suivantes ont été réalisées :

- création automatique des tables,
- insertion des données d’entrée,
- insertion des prédictions,
- suivi des employés associés aux prédictions,
- traçabilité de la version du modèle utilisée.

### 9.4 Exemple de data stockée dans la table
#### Table `employees` 

| id | employee_ref |
|----|--------------|
| 1  | 1            |

---

#### Table `inputs`

| Champ       | Valeur |
|-------------|--------|
| id          | 16     |
| employee_id | 1      |
| age         | 41     |
| revenu      | 5993   |
| n_features  | 53     |

---

#### Table `predictions`

| Champ            | Valeur                        |
|------------------|-------------------------------|
| id               | 1                             |
| input_id         | 16                            |
| employee_id      | 1                             |
| model_version_id | 1                             |
| prediction       | 1                             |
| created_at       | 2026-04-11 07:01:40.009576+00 |

---

#### Table `model_versions`

| Champ      | Valeur  |
|------------|---------|
| id         | 1       |
| model_name | XGBoost |
| version    | v1      |

------------------------------------------------------------------
### 9.5 Modélisation UML de la base

Le schéma UML de la base de données a été généré à partir des tables PostgreSQL
à l’aide de l’outil **DBeaver** connecté à la base distante hébergée sur Render.

DBeaver a permis :

- de visualiser automatiquement les relations entre les tables,
- de vérifier la cohérence du modèle relationnel,
- et d’exporter le diagramme UML pour la documentation du projet.

Le diagramme représente les relations entre :

- `employees`
- `inputs`
- `predictions`
- `model_versions`

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

------------------------------------------------------------------
## 12. Documentation technique

Une documentation technique du code est générée avec Sphinx à partir des docstrings Python.

Elle permet de documenter automatiquement les modules, fonctions et classes du projet.

------------------------------------------------------------------
## 13. Documentation utilisateur (MkDocs)

Une documentation web est générée avec MkDocs à partir de fichiers Markdown.

Elle permet de présenter :
- l’API
- l’architecture du projet
- le déploiement
- la base de données

Cette documentation est structurée en plusieurs pages pour faciliter la navigation. 