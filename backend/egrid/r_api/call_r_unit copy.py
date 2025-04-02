import requests
from egrid.models import (
    Plant,
    Unit,
)

import requests 
import logging

logger = logging.getLogger('egrid')


def sanitize_numeric(value):
    try:
        return float(value)  # Convert to a float or int
    except (ValueError, TypeError):
        return None  # Return None for invalid values

def call_r_unit():
    try:
        logger.debug('calling r unit')
        response = requests.get("http://127.0.0.1:8001/unit")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                unit_data = data.get('data', [])
                logger.debug('unit_data is: ', unit_data)
                if not unit_data:
                    logger.debug("R API returned no data. Skipping database update.")
                    return {"success": False, "message": "R API returned no data."}

                for item in unit_data:
                    # Unit is linked to a plant
                    plant_instance = Plant.objects.filter(orispl=item.get('orispl')).first()

                    if plant_instance:
                            
                        unit, created = Unit.objects.update_or_create(
                            unitid=item.get('unitid'), 
                            defaults={
                                'orispl': plant_instance,
                                'prmvr': item.get('prmvr'),  
                                'untopst': item.get('untopst'),
                                'capdflag': item.get('capdflag'),
                                'prgcode': item.get('prgcode'),
                                'botfirty': item.get('botfirty'),
                                'numgen': sanitize_numeric(item.get('numgen')),
                                'fuelu1': item.get('fuelu1'),
                                'hrsop': sanitize_numeric(item.get('hrsop')),
                            }
                        ) 

                        action = "created" if created else "updated"
                        return {f"Successfully {action} Unit with ORISPL {item.get('orispl')}."}
                    else:
                        return {"error": f"Plant with ORISPL {item.get('orispl')} not found."}
      
                return {"success": True, "message": "Data successfully inserted/updated in the Unit table."}
            else:
                logger.error(f"R API returned an error: {data.get('error')}")
                return {"error": f"R API returned an error: {data.get('error')}"}
        else:
            logger.error(f"Failed to connect to R API. Status: {response.status_code}")
            return {"error": f"Failed to connect to R API with status code {response.status_code}"}
    except Exception as e:
        logger.error(f"Error while processing R API data: {e}", exc_info=True)
        return {"error": str(e)}
