#======================================================================
# fichier qui permet à Hugging Face de savoir : quel environnement utiliser, quelles dépendances installer, quelles dépendances installer
# la DB ne sera pas dans ce conteneur
#======================================================================
# Image Python légère
FROM python:3.11-slim
 
# Répertoire de travail dans le conteneur
WORKDIR /app

# Empêche Python de créer des .pyc (fichiers compilés temporaires de Python)
ENV PYTHONDONTWRITEBYTECODE=1

# Affiche les logs Python directement
ENV PYTHONUNBUFFERED=1

# Installation de uv
RUN pip install --no-cache-dir uv

# Copier d'abord les fichiers de dépendances
COPY pyproject.toml uv.lock ./

# Installer les dépendances du projet
RUN uv sync --frozen --no-dev

# Copier le reste du code depuis le projet local vers le dossier courant dans le conteneur (/app)
COPY . .

# Exposer le port utilisé par Hugging Face Spaces
EXPOSE 7860

# Lancer l'application FastAPI
CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]