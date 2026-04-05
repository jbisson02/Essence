import requests
import gzip
import json
import os

# URL de la Régie
URL = "https://regieessencequebec.ca/stations.geojson.gz"

# IDs des stations (À vérifier dans le GeoJSON, voici des IDs probables)
# Costco Sherbrooke: 554
# Shell Portland/Érables: 1618 (Exemple)
TARGET_STATIONS = {
    "554": "Costco Sherbrooke",
    "1618": "Shell Portland/Érables"
}

def get_data():
    try:
        response = requests.get(URL, timeout=30)
        content = gzip.decompress(response.content)
        data = json.loads(content)
        
        results = []
        for feature in data['features']:
            props = feature['properties']
            s_id = str(props.get('id_station'))
            
            if s_id in TARGET_STATIONS:
                results.append({
                    "nom": TARGET_STATIONS[s_id],
                    "prix": props.get('prix_ordinaire'),
                    "maj": props.get('date_maj')
                })
        
        with open("prix.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4)
            
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    get_data()