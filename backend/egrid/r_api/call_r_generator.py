# File to communicate with the R API
import requests 
from egrid.models import Generator, Plant
import logging
import re

logger = logging.getLogger('egrid')

def sanitize_numeric(value):
    """
    Convert a value to a float if it is numeric; return None otherwise.
    """
    if value is None:
        return None
    
    # Check if the value is numeric (including numbers in string format)
    if isinstance(value, (int, float)):
        return value  # Already numeric

    # Use regex to check if it's a valid number
    if isinstance(value, str) and re.match(r'^-?\d+(\.\d+)?$', value.strip()):
        return float(value)

    return None  # Return None for invalid/non-numeric values

def populate_generator_data():
    logger.debug("*populate_generator_data")
    try:
        response = requests.get("http://127.0.0.1:8001/generator")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                gen_data = data.get('data', [])
                record_count = len(gen_data)
                logger.debug('record_count: %s', record_count)
                # logger.debug("*gen_data" + str(gen_data))

                for item in gen_data:  
                    # Generator must be linked to a plant
                    plant_instance = Plant.objects.filter(orispl=item.get('orispl')).first()
                     
                    if plant_instance:
                        generator, created = Generator.objects.update_or_create(
                            genid=sanitize_numeric(item.get('genid')),
                            defaults={ 
                                'orispl': plant_instance,  # Assign the ForeignKey instance
                                'seqgen': sanitize_numeric(item.get('seqgen')),
                            
                                # 'numblr':sanitize_numeric(item.get('numblr')),  
                                # 'genstat':sanitize_numeric(item.get('genstat')),
                                # 'prmvr':sanitize_numeric(item.get('prmvr')),   
                                # 'fuelg1':sanitize_numeric(item.get('fuelg1')), 
                                # 'namepcap':sanitize_numeric(item.get('namepcap')),
                                # 'cfact':sanitize_numeric(item.get('cfact')),   
                                # 'genntan':sanitize_numeric(item.get('genntan')),
                                # 'genntoz':sanitize_numeric(item.get('genntoz')),
                                # 'genersrc':sanitize_numeric(item.get('genersrc')),
                                # 'genyronl':sanitize_numeric(item.get('genyronl')),
                                # 'genyrret':sanitize_numeric(item.get('genyrret')),
                                # 'year':sanitize_numeric(item.get('year'))
                            }
                    )
                        
                    if created:
                        logger.info(f"New Generator created: {generator.genid}")
                    else:
                        logger.debug(f"Updated existing Generator: {generator.genid}")
                else:
                    logger.warning(f"Plant not found for orispl: {item.get('orispl')}")
                return {"success": True, "message": "Data successfully inserted into the Generator table."}
            else:
                return {"error": "R API returned an error: {}".format(data.get('error'))}
        else:
            return {"error": "Failed to connect to R API with status code {}".format(response.status_code)}
    except Exception as e:
        return {"error": str(e)}