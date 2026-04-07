from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base

# adapte le mot de passe si besoin
DATABASE_URL = "postgresql+psycopg://postgres:fk_projet5@localhost:5432/projet5_db"

# créer une connexion à la base de données (lien entre Python et PostgreSQL)
engine = create_engine(DATABASE_URL)

# session pour interagir avec la base
SessionLocal = sessionmaker(bind=engine)

# base pour les modèles (créer des tables)
Base = declarative_base()

# créer une session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()