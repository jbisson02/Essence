import requests
import json

URL = "https://regieessencequebec.ca/stations.geojson.gz"

# Tes codes postaux cibles
TARGET_POSTAL_CODES = ["J1L 0C8", "J1L 2A4", "J0B 2P0", "J0E 2L0", "J0E 1E0", "J0C 1M0" ]

def get_data():
    headers = {'User-Agent': 'Mozilla/5.0'}
    print("Téléchargement des données...")
    
    try:
        response = requests.get(URL, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        results = []
        features = data.get('features', [])

        for feature in features:
            props = feature.get('properties', {})
            cp = props.get('PostalCode', '')
            
            # On vérifie si le code postal correspond
            if cp in TARGET_POSTAL_CODES:
                nom = props.get('Name', 'Station')
                marque = props.get('brand', '')
                adresse = props.get('Address', '')
                
                # Extraction du prix "Régulier" dans la liste "Prices"
                prix_regulier = "N/A"
                prices_list = props.get('Prices', [])
                for p in prices_list:
                    if p.get('GasType') == 'Régulier':
                        prix_regulier = p.get('Price')
                        break
                
                results.append({
                    "nom": f"{marque} - {nom}",
                    "adresse": adresse,
                    "prix": prix_regulier,
                    "maj": "Aujourd'hui" # Le fichier ne semble pas avoir de date par station
                })

        print(f"Succès : {len(results)} stations trouvées.")
        
        with open("prix.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
            
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    get_data()
