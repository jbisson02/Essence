import requests
import json

# URL de la Régie
URL = "https://regieessencequebec.ca/stations.geojson.gz"

# IDs pour Sherbrooke
TARGET_STATIONS = {
    "554": "Costco Sherbrooke",
    "1618": "Shell Portland/Érables"
}

def get_data():
    print("Tentative de téléchargement...")
    response = requests.get(URL, timeout=30)
    response.raise_for_status()
    
    print("Analyse du JSON...")
    # On essaie de lire directement le JSON car le serveur ne semble plus compresser le flux
    try:
        data = response.json()
    except Exception:
        # Au cas où c'est un problème d'encodage, on force le décodage texte
        data = json.loads(response.text)
    
    results = []
    for feature in data.get('features', []):
        props = feature.get('properties', {})
        # On vérifie id_station ou id (selon la version du JSON)
        s_id = str(props.get('id_station') or props.get('id'))
        
        if s_id in TARGET_STATIONS:
            results.append({
                "nom": TARGET_STATIONS[s_id],
                "prix": props.get('prix_ordinaire') or props.get('prix'),
                "maj": props.get('date_maj') or props.get('derniere_maj')
            })
    
    print(f"Trouvé {len(results)} stations.")
    
    # Sauvegarde du résultat
    with open("prix.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    get_data()
