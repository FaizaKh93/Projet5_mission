# API

## Endpoint principal

POST `/predict`

Permet de prédire le risque d’attrition des employés.

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
