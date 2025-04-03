import requests
from egrid.models import (
    State, 
    StateAnnualCombustion, 
    StateEmissionRate, 
    StateFuelTypeEmissionRate,
    StateFuelTypeGeneration,
    StateNonBaseloadEmissionRate,
    StateResourceMix
)
import requests 
import logging
import pandas as pd 
from sqlalchemy import create_engine, text 
from django.conf import settings

logger = logging.getLogger('egrid')

def call_r_state():

    engine = create_engine(
        f"postgresql://{settings.DATABASES['default']['USER']}:{settings.DATABASES['default']['PASSWORD']}@"
        f"{settings.DATABASES['default']['HOST']}:{settings.DATABASES['default']['PORT']}/"
        f"{settings.DATABASES['default']['NAME']}"
        )   

    try:
        logger.debug('calling r state')
        response = requests.get("http://127.0.0.1:8001/state")
        data = response.json() 
     
        if response.status_code == 200 and data.get('success'):
            state_data = data.get('data', [])
            df = pd.DataFrame(state_data)
        
            df = df[['fipsst', 'pstatabb']] 
         
            try:
                with engine.connect() as conn:
                    trans = conn.begin()
                    conn.execute(text("truncate table state cascade;"))  
                    # result = conn.execute(text("SELECT COUNT(*) FROM plant;"))
                   
                    trans.commit() 
                df.to_sql('state', con=engine, if_exists='append', index=False)
                print('Success inserting state data.')
                return {"success": True, "message": "Data successfully inserted into the State table."}
            except Exception as e:
                print('Error inserting state data.', e)
                return {"error": str(e)}
              
    except Exception as e:
        logger.error(f"Error while processing R API data: {e}", exc_info=True)
        return {"error": str(e)}
        
