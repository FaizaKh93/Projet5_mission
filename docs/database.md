# Base de données

Les prédictions sont stockées dans PostgreSQL.

## Table

- id
- input_data
- prediction
- created_at

## Fonctionnement

Chaque appel à `/predict` enregistre une ligne en base. 