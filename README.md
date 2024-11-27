# 🎯 MiniProjet Python - Dashboard Interactif

## 📖 Introduction

Ce projet vise à créer un dashboard interactif en Python basé sur des données Open Data.
Il permet d’explorer, de visualiser et d’analyser des données d’intérêt public à l’aide de graphiques dynamiques et intuitifs.

## 📋 User Guide

### 🛠️ Prérequis

	•	Python 3.8 ou plus récent
	•	Les dépendances listées dans requirements.txt

### 🚀 Installation

	1.	Clonez le dépôt Git :

git clone https://github.com/Zedoww/MiniProjet.git
cd MiniProjet


	2.	Créez un environnement virtuel (recommandé) :

python -m venv .venv
source .venv/bin/activate  # Sous Windows : .venv\Scripts\activate


	3.	Installez les dépendances :

python -m pip install -r requirements.txt



▶️ Lancer le Dashboard

	1.	Exécutez le fichier principal :

python main.py


	2.	Ouvrez un navigateur et accédez à l’URL suivante :
http://127.0.0.1:8050/

## 📂 Data

### 📥 Sources des données

	•	Description : Provenance et description des jeux de données Open Data utilisés.
	•	Lien : Lien vers les données Open Data

### 📊 Structure des données

	•	Fichiers bruts : stockés dans data/raw/
	•	Fichiers nettoyés : stockés dans data/cleaned/

### 📜 Scripts associés

	•	get_data.py : Télécharge les données dans data/raw/
	•	clean_data.py : Nettoie les données et les place dans data/cleaned/

## 🛠️ Developer Guide

📂 Structure du projet

Voici l’architecture générale du projet, représentée avec Mermaid pour plus de clarté :

graph TD;
    A[main.py] --> B[config.py];
    A --> C[src/];
    C --> D[components/];
    D --> D1[header.py];
    D --> D2[footer.py];
    D --> D3[navbar.py];
    C --> E[pages/];
    E --> E1[home.py];
    E --> E2[about.py];
    E --> E3[more_complex_page/];
    E3 --> E3a[layout.py];
    E3 --> E3b[page_specific_component.py];
    C --> F[utils/];
    F --> F1[get_data.py];
    F --> F2[clean_data.py];
    A --> G[data/];
    G --> G1[raw/];
    G --> G2[cleaned/];

(N’oubliez pas d’ajouter le graphique généré par Mermaid.)

➕ Ajouter une page ou un graphique

	1.	Créez un fichier dans src/pages/ ou src/components/.
	2.	Ajoutez la logique ou les graphiques nécessaires.
	3.	Intégrez la page ou le graphique dans le layout principal (main.py).

## 📊 Rapport

Cette section mettra en avant :
	•	Les tendances observées dans les données.
	•	Les points clés des visualisations interactives.

## 📜 Copyright

Ce projet est sous licence libre.
Tout emprunt ou code externe est crédité ci-dessous :
	•	[Expliquer les emprunts éventuels et leurs sources]

	Astuce : Pour visualiser le diagramme Mermaid, vous pouvez utiliser l’éditeur en ligne Mermaid Live Editor.