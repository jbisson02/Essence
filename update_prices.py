
import requests
import json

URL = "https://regieessencequebec.ca/stations.geojson.gz"
TARGET_POSTAL_CODES = ["J1L 0C8", "J1L 2A4"]
#TARGET_POSTAL_CODES = ["J1L 0C8", "J1L 2A4", "J0B 2P0", "J0E 2L0", "J0E 1E0", "J0C 1M0" ]

def get_data():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(URL, headers=headers, timeout=30)
        data = response.json()
        
        results = []
        all_prices = []
        features = data.get('features', [])

        for feature in features:
            props = feature.get('properties', {})
            
            # Extraction du prix régulier pour statistiques
            prix_val = None
            for p in props.get('Prices', []):
                if p.get('GasType') == 'Régulier' and p.get('IsAvailable'):
                    try:
                        # On enlève le "¢" et on convertit en nombre
                        prix_val = float(p.get('Price').replace('¢', ''))
                        all_prices.append(prix_val)
                    except:
                        pass
            
            # Filtrage pour tes stations (Sherbrooke)
            if props.get('PostalCode') in TARGET_POSTAL_CODES:
                results.append({
                    "nom": f"{props.get('brand', '')} - {props.get('Name', '')}",
                    "adresse": props.get('Address', ''),
                    "prix": f"{prix_val}¢" if prix_val else "N/A",
                    "maj": "Récemment"
                })

        # Calcul des stats provinciales
        stats = {
            "min": f"{min(all_prices)}¢" if all_prices else "N/A",
            "max": f"{max(all_prices)}¢" if all_prices else "N/A"
        }

        # On sauvegarde un dictionnaire contenant les deux infos
        final_data = {
            "stations": results,
            "stats": stats
        }

        with open("prix.json", "w", encoding="utf-8") as f:
            json.dump(final_data, f, indent=4, ensure_ascii=False)
            
        print("Mise à jour réussie.")
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    get_data()
