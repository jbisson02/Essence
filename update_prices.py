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
        
        # Extraction de la date de génération du fichier (Metadata)
        file_date = data.get('metadata', {}).get('generated_at', 'Inconnue')
        
        results = []
        min_station = None
        max_station = None
        min_price = float('inf')
        max_price = float('-inf')

        features = data.get('features', [])

        for feature in features:
            props = feature.get('properties', {})
            
            current_price = None
            for p in props.get('Prices', []):
                if p.get('GasType') == 'Régulier' and p.get('IsAvailable'):
                    try:
                        current_price = float(p.get('Price').replace('¢', ''))
                    except:
                        continue
            
            if current_price is None:
                continue

            if current_price < min_price:
                min_price = current_price
                min_station = {"nom": f"{props.get('brand', '')} - {props.get('Name', '')}", "adresse": props.get('Address', ''), "prix": f"{current_price}¢"}
            
            if current_price > max_price:
                max_price = current_price
                max_station = {"nom": f"{props.get('brand', '')} - {props.get('Name', '')}", "adresse": props.get('Address', ''), "prix": f"{current_price}¢"}

            if props.get('PostalCode') in TARGET_POSTAL_CODES:
                results.append({
                    "nom": f"{props.get('brand', '')} - {props.get('Name', '')}",
                    "adresse": props.get('Address', ''),
                    "prix": f"{current_price}¢"
                })

        final_data = {
            "file_generated_at": file_date,
            "stations": results,
            "stats": {"min": min_station, "max": max_station}
        }

        with open("prix.json", "w", encoding="utf-8") as f:
            json.dump(final_data, f, indent=4, ensure_ascii=False)
            
        print(f"Mise à jour réussie. Fichier généré le : {file_date}")
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    get_data()
