import requests 
from egrid.models import State, Subregion 
import requests 
import logging

logger = logging.getLogger('egrid')


def sanitize_numeric(value):
    try:
        return float(value)  # Convert to a float or int
    except (ValueError, TypeError):
        return None  # Return None for invalid values

def call_r_subregion():
    try:
        response = requests.get("http://127.0.0.1:8001/subregion")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                subrgn_data = data.get('data', [])
                logger.debug('subrgn_data is: ', subrgn_data)
                if not subrgn_data:
                    logger.warning("R API returned no data. Skipping database update.")
                    return {"success": False, "message": "R API returned no data."}

                for item in subrgn_data:
                    subregion, created = Subregion.objects.update_or_create(
                        subrgn=item.get('subrgn'), 
                        defaults={
                            'srname':item.get('srname'), 
                        }
                    ) 

                    if created:
                        logger.info(f"Inserted new plant: {subregion.subrgn}")
                    else:
                        logger.info(f"Updated existing plant: {subregion.subrgn}")

                return {"success": True, "message": "Data successfully inserted/updated in the Subregion table."}
            else:
                logger.error(f"R API returned an error: {data.get('error')}")
                return {"error": f"R API returned an error: {data.get('error')}"}
        else:
            logger.error(f"Failed to connect to R API. Status: {response.status_code}")
            return {"error": f"Failed to connect to R API with status code {response.status_code}"}
    except Exception as e:
        logger.error(f"Error while processing R API data: {e}", exc_info=True)
        return {"error": str(e)}
