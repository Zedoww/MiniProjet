import pandas as pd

def clean_weather_data(input_file, output_file):
    """
    Nettoie les données météorologiques pour ne conserver que les données de la France hexagonale
    et les colonnes spécifiques : température, vitesse du vent, précipitations.

    Args:
        input_file (str): Chemin vers le fichier CSV brut.
        output_file (str): Chemin où sauvegarder le fichier nettoyé.
    """
    # Charger les données brutes
    try:
        df = pd.read_csv(input_file, sep=";")
    except FileNotFoundError:
        print(f"Erreur : Le fichier {input_file} est introuvable.")
        return

    # Filtrer les données pour garder uniquement celles de la France hexagonale
    # En supposant que la colonne 'region (name)' identifie les régions
    france_regions = ["Île-de-France", "Bretagne", "Normandie", "Provence-Alpes-Côte d'Azur",
                      "Nouvelle-Aquitaine", "Occitanie", "Auvergne-Rhône-Alpes", "Bourgogne-Franche-Comté",
                      "Grand Est", "Hauts-de-France", "Centre-Val de Loire", "Pays de la Loire"]
    df = df[df["region (name)"].isin(france_regions)]

    # Sélectionner uniquement les colonnes nécessaires
    columns_to_keep = [
        "Température (°C)",
        "Vitesse du vent moyen 10 mn",
        "Précipitations dans les 24 dernières heures",
        "Nom",  # Optionnel : pour identifier les stations
        "Date"  # Optionnel : pour conserver une dimension temporelle
    ]
    df_cleaned = df[columns_to_keep]

    # Enregistrer le fichier nettoyé
    df_cleaned.to_csv(output_file, sep=";", index=False)
    print(f"Fichier nettoyé enregistré dans : {output_file}")

# Exemple d'utilisation
if __name__ == "__main__":
    raw_file = "data/raw/donnees-synop-essentielles-omm.csv"
    cleaned_file = "data/cleaned/cleaned_data.csv"
    clean_weather_data(raw_file, cleaned_file)