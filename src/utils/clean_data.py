import pandas as pd

def clean_raw_data(input_path, output_path):
    # Charger les données
    data = pd.read_csv(input_path, delimiter=';')
    
    # Convertir la colonne Date en type datetime
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce', utc=True)
    
    # Supprimer les lignes avec des valeurs manquantes et les duplicatas
    data = data.dropna(subset=['Date', 'Température (°C)', 'Précipitations dans les 24 dernières heures', 'Vitesse du vent moyen 10 mn', 'Pression au niveau mer']).drop_duplicates()
    
    # Filtrer les valeurs valides (température raisonnable) et garder les données de la France métropolitaine
    data = data[(data['Température (°C)'] >= -50) & (data['Température (°C)'] <= 60)]
    data = data[data['region (name)'].str.contains(r'France|Île-de-France|Provence-Alpes-Côte d\'Azur|Grand Est|Bourgogne-Franche-Comté|Bretagne|Normandie|Nouvelle-Aquitaine|Occitanie|Hauts-de-France|Pays de la Loire|Centre-Val de Loire', case=False, na=False)]
    
    # Garder seulement les colonnes nécessaires
    columns_needed = ['Date', 'Température (°C)', 'Précipitations dans les 24 dernières heures', 'Vitesse du vent moyen 10 mn', 'Pression au niveau mer']
    data = data[columns_needed]
    
    # Renommer les colonnes pour simplifier l'utilisation dans le dashboard
    data = data.rename(columns={
        'Température (°C)': 'Temperature',
        'Précipitations dans les 24 dernières heures': 'Precipitation',
        'Vitesse du vent moyen 10 mn': 'WindSpeed',
        'Pression au niveau mer': 'Pressure'
    })

    # Convertir en float et arrondir les valeurs de précipitation et de température
    data['Precipitation'] = data['Precipitation'].astype(float).round(2)
    data['Temperature'] = data['Temperature'].astype(float).round(2)
    
    # Sauvegarder les données nettoyées
    data.to_csv(output_path, index=False)

if __name__ == "__main__":
    input_path = "data/raw/raw.csv"
    output_path = "data/cleaned/cleaneddata.csv"
    clean_raw_data(input_path, output_path)
