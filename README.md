# Auteur

Faiza Khelladi  
Formation Data Scientist – Machine Learning

------------------------------------------------------------------
# Prédiction de l’attrition des employés dans une ESN

## Description du projet

Ce projet a pour objectif d’identifier les causes du départ des employés (attrition) au sein d’une entreprise de services numériques (ESN) et de développer un modèle de ML permettant de prédire les risques de démission.

L’objectif est d’aider les équipes RH à :

- anticiper les départs des employés
- comprendre les facteurs expliquant l’attrition
- mettre en place des actions pour réduire le turnover et préserver les talents

------------------------------------------------------------------

# Contexte

L’entreprise fait face à un taux de démission élevé, ce qui entraîne :

- une perte de talents
- des coûts de recrutement importants
- une perte de connaissances internes

Une analyse des données RH a été réalisée afin :

1. d’identifier les causes des départs
2. de construire un modèle de prédiction du risque de départ des employés

------------------------------------------------------------------

# Données utilisées

Trois sources de données ont été utilisées :

## Données SIRH

Informations sur les employés :

- ancienneté dans l’entreprise
- revenu mensuel
- département
- poste
- âge
- etc.

## Évaluations annuelles

Informations sur les performances et la satisfaction :

- note d’évaluation précédente
- satisfaction dans l’équipe
- satisfaction dans l’environnement de travail
- etc.

## Sondage des employés

Informations issues des enquêtes internes :

- fréquence des déplacements
- participation aux plans d’épargne entreprise
- heures supplémentaires
- domaine d’étude
- etc.

Les datasets ont été fusionnés pour créer une base de données unique de **1470 employés**.

------------------------------------------------------------------

# Analyse exploratoire des données

Une analyse descriptive a été réalisée afin d'étudier :

- la distribution des variables numériques
- la répartition des variables catégorielles
- les relations entre variables et départs d’employés

------------------------------------------------------------------
# Préparation des données

Plusieurs étapes de **feature engineering** ont été réalisées.

Exemples de variables créées :

- variation de la note d’évaluation
- moyenne des scores de satisfaction
- vote de satisfaction
- ratio satisfaction / ancienneté
- risque de burnout
- ratio salaire / salaire moyen par poste
- ratio salaire / salaire moyen par département
- mobilité interne
- ratio de stagnation

Ces variables permettent de capturer des signaux liés au départ des employés.

------------------------------------------------------------------

# Encodage des données

Les variables catégorielles ont été transformées avec :

- OneHotEncoder
- mapping pour certaines variables ordinales

Variable cible :

a_quitte_l_entreprise

0 = employé reste  
1 = employé quitte l’entreprise

------------------------------------------------------------------

# Modélisation

Plusieurs modèles supervisés ont été testés :

-------------------------------------
## Dummy Classifier

Modèle de référence pour comparer les performances.

-------------------------------------
## Régression Logistique

Amélioration des performances mais présence de faux négatifs.

-------------------------------------
## XGBoost

Le modèle XGBoost a donné les meilleures performances.

Optimisations réalisées :

- équilibrage des classes
- stratification des données
- optimisation du seuil

Seuil optimal : **0.711**

Score F2 : **0.613**

------------------------------------------------------------------

# Interprétation du modèle

## Importance globale des variables

Variables dominantes :

- ancienneté dans l’entreprise
- salaire moyen par poste
- salaire moyen par département
- participation au plan d’épargne entreprise

## Interprétation locale avec SHAP

Les analyses montrent que :

- les heures supplémentaires augmentent le risque de démission
- une faible satisfaction des employés favorise le départ
- un salaire relativement moins compétitif augmente la probabilité de quitter l’entreprise

------------------------------------------------------------------
# Résultats

Le modèle permet :

- d’anticiper les départs
- d’identifier les facteurs d’attrition
- d’aider les équipes RH à mettre en place des actions de rétention

------------------------------------------------------------------

# Perspectives

Améliorations possibles :

- intégrer de nouvelles données RH
- améliorer la précision du modèle
- déployer une API d’aide à la décision pour les équipes RH

------------------------------------------------------------------

# Structure du projet

```
Projet5_mission
│
├── data
├── functions
├── notebooks
├── presentation
├── pyproject.toml
└── README.md
```

---

