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
    # On ajoute des entêtes pour imiter un vrai navigateur
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    print("Tentative de téléchargement avec User-Agent...")
    
    try:
        # On télécharge avec les entêtes
        response = requests.get(URL, headers=headers, timeout=30)
        response.raise_for_status()
        
        print("Analyse du contenu...")
        # Requests gère automatiquement la décompression si le serveur envoie du GZIP
        data = response.json()
        
        results = []
        for feature in data.get('features', []):
            props = feature.get('properties', {})
            # On vérifie les deux noms de clés possibles
            s_id = str(props.get('id_station') or props.get('id'))
            
            if s_id in TARGET_STATIONS:
                results.append({
                    "nom": TARGET_STATIONS[s_id],
                    "prix": props.get('prix_ordinaire') or props.get('prix'),
                    "maj": props.get('date_maj') or props.get('derniere_maj')
                })
        
        print(f"Succès ! Trouvé {len(results)} stations.")
        
        with open("prix.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
            
    except requests.exceptions.HTTPError as e:
        print(f"Erreur HTTP (Probablement encore un blocage) : {e}")
    except Exception as e:
        print(f"Autre erreur : {e}")

if __name__ == "__main__":
    get_data()
