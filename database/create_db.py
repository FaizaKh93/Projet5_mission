from sqlalchemy import Column, Integer, Float, DateTime, JSON, String, ForeignKey  
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship  # permet de créer des relations entre tables

from database.db_config import Base, engine


# =========================
# Table des employés
# =========================
class Employee(Base):
    __tablename__ = "employees"  

    # clé primaire
    id = Column(Integer, primary_key=True, index=True)  

    # identifiant unique de l’employé (ex: ID RH)
    employee_ref = Column(String, unique=True, index=True, nullable=False)  

   # relation : un employé peut avoir plusieurs inputs
    inputs = relationship("InputDataDB", back_populates="employee")  
 


# =========================
# Table des versions du modèle
# =========================
class ModelVersion(Base):
    __tablename__ = "model_versions"

    # clé primaire
    id = Column(Integer, primary_key=True, index=True)

    model_name = Column(String, nullable=False)  

    # version du modèle (ex: v1, v2)
    version = Column(String, nullable=False)  

    # date de création de la version
    created_at = Column(DateTime(timezone=True), server_default=func.now())  

    # relation : une version peut générer plusieurs prédictions
    predictions = relationship("Prediction", back_populates="model_version")  


# =========================
# Table des inputs (données envoyées au modèle)
# =========================
class InputDataDB(Base):
    __tablename__ = "inputs"

    # clé primaire
    id = Column(Integer, primary_key=True, index=True)

    # clé étrangère vers la table employees
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)  

    # stockage des données d'entrée (features)
    input_data = Column(JSON, nullable=False)  

    # quelques inputs à analyser 
    age = Column(Float, nullable=True) 
    revenu = Column(Float, nullable=True)

    # nombre de variables 
    n_features = Column(Integer, nullable=False)  

    # date d'insertion
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relation inverse vers Employee
    employee = relationship("Employee", back_populates="inputs")  

    # relation 1-1 : un input → une prédiction
    prediction = relationship("Prediction", back_populates="input", uselist=False)  


# =========================
# Table des prédictions
# =========================
class Prediction(Base):
    __tablename__ = "predictions"

    # clé primaire
    id = Column(Integer, primary_key=True, index=True)

     # lien vers les données utilisées pour la prédiction
    input_id = Column(Integer, ForeignKey("inputs.id"), nullable=False) 

    # lien vers l'id de l'employer 
    employee_id = Column(Integer, ForeignKey("employees.id")) 
 
    # lien vers la version du modèle
    model_version_id = Column(Integer, ForeignKey("model_versions.id"), nullable=True)  

    # valeur prédite
    prediction = Column(Float, nullable=False)  

    # date de la prédiction
    created_at = Column(DateTime(timezone=True), server_default=func.now())  

    # relation vers les données d’entrée
    input = relationship("InputDataDB", back_populates="prediction")  

    # relation vers la version du modèle
    model_version = relationship("ModelVersion", back_populates="predictions")  


# =========================
# Création des tables
# =========================
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine) # créer physiquement la table dans PostgreSQL
    print("Tables created successfully")