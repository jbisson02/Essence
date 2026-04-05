import requests
import json

URL = "https://regieessencequebec.ca/stations.geojson.gz"

# Liste des codes postaux cibles (sans espaces pour faciliter la comparaison)
TARGET_POSTAL_CODES = ["J1L0C8", "J1L2A4"]

def get_data():
    headers = {'User-Agent': 'Mozilla/5.0'}
    print("Téléchargement des données de la Régie...")
    
    try:
        response = requests.get(URL, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for feature in data.get('features', []):
            props = feature.get('properties', {})
            
            # On récupère le code postal et on enlève les espaces pour comparer
            raw_pc = str(props.get('PostalCode', '')).replace(" ", "").upper()
            
            if raw_pc in TARGET_POSTAL_CODES:
                # Identification simplifiée basée sur le code postal pour l'affichage
                nom_station = props.get('nom_station') or props.get('marque') or "Station"
                adresse = props.get('adresse', '')
                
                results.append({
                    "nom": f"{nom_station} ({adresse})",
                    "prix": props.get('prix_ordinaire') or props.get('prix'),
                    "maj": props.get('date_maj') or props.get('derniere_maj') or "Récemment",
                    "cp": props.get('code_postal')
                })
        
        # Tri du moins cher au plus cher
        results.sort(key=lambda x: float(x['prix']) if x['prix'] else 999)

        print(f"Succès ! {len(results)} station(s) trouvée(s) pour les codes postaux demandés.")
        
        with open("prix.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
            
    except Exception as e:
        print(f"Erreur lors de l'exécution : {e}")

if __name__ == "__main__":
    get_data()
