import requests
from egrid.models import NercRegion
from sqlalchemy import text 
import requests 
import logging 
import pandas as pd 

logger = logging.getLogger('egrid')
 
def call_r_nerc(engine=None, api_url=None): 
    try:
        response = requests.get(f"{api_url}nerc")
        data = response.json() 
        
        if response.status_code == 200 and data.get('success'):
            nerc_data = data.get('data', [])
            df = pd.DataFrame(nerc_data)
        
            df = df[['nerc', 'nercname']] 
         
            try:
                with engine.connect() as conn:
                    trans = conn.begin()
                    conn.execute(text("truncate table nerc cascade;"))  
                    # result = conn.execute(text("SELECT COUNT(*) FROM plant;"))
                   
                    trans.commit() 
                df.to_sql('nerc', con=engine, if_exists='append', index=False)
                print('Success inserting nerc data.')
                return {"success": True, "message": "Data successfully inserted into the NERC table."}
            except Exception as e:
                print('Error inserting nerc data.', e)
                return {"error": str(e)}
              
    except Exception as e:
        logger.error(f"Error while processing R API data: {e}", exc_info=True)
        return {"error": str(e)}
