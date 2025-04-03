# File to communicate with the R API
import requests 
from egrid.models import Generator, Plant
import logging 
import pandas as pd
from django.db import connection
from sqlalchemy import create_engine, text

logger = logging.getLogger('egrid')
 
from django.conf import settings
  
def populate_generator_data(engine=None, api_url=None):
    print('populate_generator_data')
    logger.debug("*populate_generator_data")
     
    try:
        response = requests.get(f"{api_url}generator")
        data = response.json()  
        if response.status_code == 200 and data.get('success'):
            gen_data = data.get('data', [])
            df = pd.DataFrame(gen_data)
            # print('df', df.head()) # for debugging
            df = df[['seqgen', 'genid', 'orispl']] 
           
            try: 
                with engine.connect() as conn:
                    trans = conn.begin()
                    conn.execute(text("truncate table generator cascade;")) 
                    trans.commit() 

                df.to_sql('generator', con=engine, if_exists='append', index=False)
                print('success')
                return {"success": True, "message": "Data successfully inserted into the Generator table."}
            except Exception as e:
                print('error', e)
                return {"error": str(e)}
        else:
            print('error')
            return {"error": "R API returned an error: {}".format(data.get('error'))} 
    except Exception as e:
        return {"error": str(e)}