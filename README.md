# Conseiller ENSTP

Un chatbot intelligent pour aider les étudiants de l'ENSTP à choisir entre les départements DMS et DIB après leur cycle préparatoire.

## Fonctionnalités

- Interface de chat interactive
- Répond aux questions sur les cours, les débouchés et les aptitudes requises pour chaque département
- Fournit des conseils personnalisés basés sur les intérêts et aptitudes de l'étudiant
- Aide à la prise de décision pour le choix de spécialisation

## Installation

1. Clonez ce dépôt
2. Installez les dépendances:
```
pip install -r requirements.txt
```
3. Créez un fichier `.env` avec votre clé API Google Gemini:
```
GOOGLE_API_KEY=votre-clé-api
```

## Démarrage

```
streamlit run app.py
```

## Déploiement

Pour déployer sur Streamlit Cloud:
1. Connectez-vous à votre compte Streamlit Cloud
2. Créez une nouvelle app en pointant vers ce dépôt
3. Configurez la variable d'environnement `GOOGLE_API_KEY` dans les paramètres de l'app

## Créé par

Cherif Tas

## Technologies utilisées

- Streamlit
- Google Gemini AI
- Python 