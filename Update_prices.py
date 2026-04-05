import requests
import gzip
import json

URL = "https://regieessencequebec.ca/stations.geojson.gz"

# IDs confirmés pour Sherbrooke
TARGET_STATIONS = {
    "554": "Costco Sherbrooke",
    "1618": "Shell Portland/Érables"
}

def get_data():
    print("Tentative de téléchargement...")
    response = requests.get(URL, timeout=30)
    response.raise_for_status() # Génère une erreur si le site est down
    
    print("Décompression...")
    content = gzip.decompress(response.content)
    data = json.loads(content)
    
    results = []
    for feature in data['features']:
        props = feature['properties']
        # On convertit en string pour comparer avec nos clés TARGET_STATIONS
        s_id = str(props.get('id_station'))
        
        if s_id in TARGET_STATIONS:
            results.append({
                "nom": TARGET_STATIONS[s_id],
                "prix": props.get('prix_ordinaire'),
                "maj": props.get('date_maj')
            })
    
    print(f"Trouvé {len(results)} stations.")
    with open("prix.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    get_data()
