import requests
from egrid.models import NercRegion

import requests 
import logging

logger = logging.getLogger('egrid')


def sanitize_numeric(value):
    try:
        return float(value)  # Convert to a float or int
    except (ValueError, TypeError):
        return None  # Return None for invalid values

def call_r_nerc():
    try:
        response = requests.get("http://127.0.0.1:8001/nerc")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                nerc_data = data.get('data', [])
                logger.debug('nerc_data is: ', nerc_data)
                if not nerc_data:
                    logger.warning("R API returned no data. Skipping database update.")
                    return {"success": False, "message": "R API returned no data."}

                for item in nerc_data:
                    nerc_region, created = NercRegion.objects.update_or_create(
                        nerc=item.get('nerc'), 
                        defaults={
                            'nerc_name':item.get('nerc'), 
                        }
                    ) 

                    if created:
                        logger.info(f"Inserted new plant: {nerc_region.nerc}")
                    else:
                        logger.info(f"Updated existing plant: {nerc_region.nerc}")

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
