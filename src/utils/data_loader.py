import pandas as pd
import json

def load_cleaned_data(filepath="data/cleaned/cleaneddata.csv"):
    data = pd.read_csv(filepath)
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce', utc=True)
    data.dropna(subset=['Date'], inplace=True)
    return data

def load_regions_geojson(filepath="data/regions.geojson"):
    with open(filepath, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)
    return geojson_data

def load_departements_geojson(filepath="data/departements.geojson"):
    with open(filepath, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)
    return geojson_data

