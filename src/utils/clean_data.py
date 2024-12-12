import pandas as pd

def clean_raw_data(input_path, output_path):
    # Charger les données
    data = pd.read_csv(input_path, delimiter=';', encoding='utf-8')

    # Supprimer les espaces en début et fin des noms de colonnes
    data.columns = data.columns.str.strip()

    # Garder uniquement les colonnes spécifiées
    colonnes_conservees = [
        'Date',
        'Température',
        'Température maximale sur 12 heures',
        'Température minimale sur 12 heures',
        'Température maximale sur 24 heures',
        'Température minimale sur 24 heures',
        'Précipitations dans la dernière heure',
        'Précipitations dans les 3 dernières heures',
        'Précipitations dans les 6 dernières heures',
        'Précipitations dans les 12 dernières heures',
        'Précipitations dans les 24 dernières heures',
        'Vitesse du vent moyen 10 mn',
        'Rafale sur les 10 dernières minutes',
        'Latitude',
        'Longitude',
        'communes (name)',
        'department (code)',
        'region (code)',
        
    ]

    # Sélectionner uniquement les colonnes disponibles
    colonnes_disponibles = [col for col in colonnes_conservees if col in data.columns]
    data = data[colonnes_disponibles]

    # Filtrer pour garder uniquement les données de la France métropolitaine
    if 'department (code)' in data.columns:
        # Codes des départements de la France métropolitaine (01 à 95, y compris '2A' et '2B' pour la Corse)
        departements_metropole = [str(i).zfill(2) for i in range(1, 96) if i != 20] + ['2A', '2B']
        data = data[data['department (code)'].astype(str).isin(departements_metropole)]
    else:
        # Si 'department (code)' n'est pas disponible, filtrer par coordonnées géographiques
        data = data[(data['Latitude'].between(41.0, 51.0)) & (data['Longitude'].between(-5.0, 9.0))]

    # Sauvegarder les données nettoyées
    data.to_csv(output_path, index=False)

if __name__ == "__main__":
    input_path = "data/raw/raw.csv"
    output_path = "data/cleaned/cleaneddata.csv"
    clean_raw_data(input_path, output_path)