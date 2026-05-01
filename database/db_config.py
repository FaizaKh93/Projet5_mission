"""
Configuration de la base de données.

Ce module gère la connexion à la base PostgreSQL via SQLAlchemy,
ainsi que la création des sessions utilisées dans l'application FastAPI.
"""

import os
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de connexion à la base de données : Priorité à la variable d'environnement DATABASE_URL, sinon, on utilise une URL locale par défaut pour le développement
DATABASE_URL = os.getenv("DATABASE_URL","postgresql+psycopg://postgres:fk_projet5@localhost:5432/projet5_db")

# ancien : local

# créer une connexion à la base de données (lien entre Python et PostgreSQL)
engine = create_engine(DATABASE_URL)

# session pour interagir avec la base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#SessionLocal = sessionmaker(bind=engine)

# base pour les modèles (créer des tables)
Base = declarative_base()

# créer une session de base de données
def get_db():
    """
    Génère une session de base de données.

    Cette fonction est utilisée comme dépendance dans FastAPI
    pour fournir une session active à chaque requête.

    Yields:
        Session: Session SQLAlchemy permettant d'exécuter des requêtes.

    Fonctionnement:
        - ouvre une session
        - la fournit à l'endpoint
        - ferme la session après utilisation
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  