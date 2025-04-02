import requests
from egrid.models import NercRegion
from sqlalchemy import create_engine, text 
import requests 
import logging
from django.conf import settings
import pandas as pd 

logger = logging.getLogger('egrid')
 
def call_r_nerc():

    engine = create_engine(
    f"postgresql://{settings.DATABASES['default']['USER']}:{settings.DATABASES['default']['PASSWORD']}@"
    f"{settings.DATABASES['default']['HOST']}:{settings.DATABASES['default']['PORT']}/"
    f"{settings.DATABASES['default']['NAME']}"
    ) 

    try:
        response = requests.get("http://127.0.0.1:8001/nerc")
        data = response.json() 

        if response.status_code == 200 and data.get('success'):
            nerc_data = data.get('data', [])
            df = pd.DataFrame(nerc_data)
        
            df = df[['nerc', 'nercname']] 
         
            try:
                with engine.connect() as conn:
                    trans = conn.begin()
                    conn.execute(text("truncate table plant cascade;"))  
                    # result = conn.execute(text("SELECT COUNT(*) FROM plant;"))
                   
                    trans.commit() 
                df.to_sql('plant', con=engine, if_exists='append', index=False)
                print('Success inserting plant data.')
                return {"success": True, "message": "Data successfully inserted into the Generator table."}
            except Exception as e:
                print('Error inserting plant data.', e)
                return {"error": str(e)}
              
    except Exception as e:
        logger.error(f"Error while processing R API data: {e}", exc_info=True)
        return {"error": str(e)}

 
    #     if response.status_code == 200:
    #         data = response.json()
    #         if data.get('success'):
    #             nerc_data = data.get('data', [])
    #             logger.debug('nerc_data is: ', nerc_data)
    #             if not nerc_data:
    #                 logger.warning("R API returned no data. Skipping database update.")
    #                 return {"success": False, "message": "R API returned no data."}

    #             for item in nerc_data:
    #                 nerc_region, created = NercRegion.objects.update_or_create(
    #                     nerc=item.get('nerc'), 
    #                     defaults={
    #                         'nerc_name':item.get('nerc'), 
    #                     }
    #                 ) 

    #                 if created:
    #                     logger.info(f"Inserted new plant: {nerc_region.nerc}")
    #                 else:
    #                     logger.info(f"Updated existing plant: {nerc_region.nerc}")

    #             return {"success": True, "message": "Data successfully inserted/updated in the Plant table."}
    #         else:
    #             logger.error(f"R API returned an error: {data.get('error')}")
    #             return {"error": f"R API returned an error: {data.get('error')}"}
    #     else:
    #         logger.error(f"Failed to connect to R API. Status: {response.status_code}")
    #         return {"error": f"Failed to connect to R API with status code {response.status_code}"}
    # except Exception as e:
    #     logger.error(f"Error while processing R API data: {e}", exc_info=True)
    #     return {"error": str(e)}
