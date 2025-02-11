from egrid.models import Plant
import requests
import logging

logger = logging.getLogger('egrid')


def sanitize_numeric(value):
    try:
        return float(value)  # Convert to a float or int
    except (ValueError, TypeError):
        return None  # Return None for invalid values

def call_r_plant():
    try:
        response = requests.get("http://127.0.0.1:8001/plant")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                plant_data = data.get('data', [])

                if not plant_data:
                    logger.warning("R API returned no data. Skipping database update.")
                    return {"success": False, "message": "R API returned no data."}

                for item in plant_data:
                    plant, created = Plant.objects.update_or_create(
                        orispl=item.get('orispl'), 
                        defaults={
                            'seqplt':item.get('seqplt'),
                            'pstatabb': item.get('pstatabb'),
                            'fipsst': item.get('fipsst'),
                            'plant_name': item.get('plant_name'),
                            'oprcode': item.get('oprcode'),
                            'utlsrvid': item.get('utlsrvid'),
                            'sector_id': item.get('sector_id'),
                            'bacode': item.get('bacode'),
                            'nerc': item.get('nerc'),
                            'fipscnty': item.get('fipscnty'),
                            'lat': item.get('lat'),
                            'lon': item.get('lon'),
                            'numunt': item.get('numunt'),
                            'numgen': item.get('numgen'),
                            'plprmfl': item.get('plprmfl'),
                            'plfuelct': item.get('plfuelct'),
                            'coalflagind': item.get('coalflagind'),
                            'subrgn_id': item.get('subrgn_id'),
                            'year': item.get('year')
                        }
                    )
  
                    # Logging each insert/update
                    if created:
                        logger.info(f"Inserted new plant: {plant.orispl}")
                    else:
                        logger.info(f"Updated existing plant: {plant.orispl}")

                return {"success": True, "message": "Data successfully inserted/updated in the Plant table."}
            else:
                logger.error(f"R API returned an error: {data.get('error')}")
                return {"error": f"R API returned an error: {data.get('error')}"}
        else:
            logger.error(f"Failed to connect to R API. Status: {response.status_code}")
            return {"error": f"Failed to connect to R API with status code {response.status_code}"}
    except Exception as e:
        logger.error(f"Error while processing R API data: {e}", exc_info=True)
        return {"error": str(e)}
