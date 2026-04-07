from sqlalchemy import Column, Integer, Float, DateTime, JSON
from sqlalchemy.sql import func

from database.db_config import Base, engine


# table pour stocker les prédictions
class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)

    # données d'entrée envoyées au modèle (une ligne / un employé)
    input_data = Column(JSON)

    # nombre de features (utile pour debug)
    n_features = Column(Integer)

    # valeur prédite
    prediction = Column(Float)

    # date d'enregistrement
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# créer les tables dans la base
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine) # créer physiquement la table dans PostgreSQL
    print("Tables created successfully")

