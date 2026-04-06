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
        
        file_date = data.get('metadata', {}).get('generated_at', 'Inconnue')
        
        # Structure pour regrouper par ville
        villes = {}
        min_station = None
        max_station = None
        min_price = float('inf')
        max_price = float('-inf')

        features = data.get('features', [])

        for feature in features:
            props = feature.get('properties', {})
            
            # Extraction du prix
            current_price_str = "N/A"
            current_price_num = None
            for p in props.get('Prices', []):
                if p.get('GasType') == 'Régulier' and p.get('IsAvailable'):
                    current_price_str = p.get('Price')
                    try:
                        current_price_num = float(current_price_str.replace('¢', ''))
                    except:
                        continue
            
            if current_price_num is None:
                continue

            # Stats provinciales
            if current_price_num < min_price:
                min_price = current_price_num
                min_station = {"nom": f"{props.get('brand', '')} - {props.get('Name', '')}", "adresse": props.get('Address', ''), "prix": current_price_str}
            if current_price_num > max_price:
                max_price = current_price_num
                max_station = {"nom": f"{props.get('brand', '')} - {props.get('Name', '')}", "adresse": props.get('Address', ''), "prix": current_price_str}

            # Filtrage par Code Postal (Sherbrooke) ou tu peux décider d'inclure tout
            if props.get('PostalCode') in TARGET_POSTAL_CODES:
                # On extrait la ville de l'adresse (ex: "Rue, Ville")
                full_address = props.get('Address', '')
                ville = full_address.split(',')[-1].strip() if ',' in full_address else "Autres"
                
                if ville not in villes:
                    villes[ville] = []
                
                villes[ville].append({
                    "nom": f"{props.get('brand', '')} - {props.get('Name', '')}",
                    "adresse": full_address,
                    "prix": current_price_str
                })

        final_data = {
            "file_generated_at": file_date,
            "villes": villes,
            "stats": {"min": min_station, "max": max_station}
        }

        with open("prix.json", "w", encoding="utf-8") as f:
            json.dump(final_data, f, indent=4, ensure_ascii=False)
            
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    get_data()
