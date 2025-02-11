from egrid.logic.queries.plant_queries import get_all_plants, create_or_update_plant
import requests

USE_R_API = True  # Dynamically toggle between R and DB (could use settings)

def get_plant_data():
    """Fetch plant data dynamically, either from R API or database."""
    if USE_R_API:
        return call_r_plant()
    return list(get_all_plants())

def call_r_plant():
    """Fetch plant data from the R API."""
    try:
        response = requests.get("http://127.0.0.1:8001/plant")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                return data.get('data', [])
    except requests.exceptions.RequestException as e:
        print(f"Error calling R API: {e}")
    return []

def sync_r_to_db():
    """Fetch data from R API and sync it to the database."""
    plant_data = call_r_plant()
    for item in plant_data:
        create_or_update_plant(item)
