from egrid.models import SubrgnAnnualCombustion, Subregion, SubrgnEmissionRate, SubrgnFuelTypeEmissionRate 
import requests 
import logging
import pandas as pd 
from sqlalchemy import create_engine, text 
from django.conf import settings
logger = logging.getLogger('egrid')

def call_r_subregion():

    engine = create_engine(
    f"postgresql://{settings.DATABASES['default']['USER']}:{settings.DATABASES['default']['PASSWORD']}@"
    f"{settings.DATABASES['default']['HOST']}:{settings.DATABASES['default']['PORT']}/"
    f"{settings.DATABASES['default']['NAME']}"
    ) 

    try:
        response = requests.get("http://127.0.0.1:8001/subregion")
        data = response.json() 

        if response.status_code == 200 and data.get('success'):
            subregion_data = data.get('data', [])
            df = pd.DataFrame(subregion_data)
        
            df = df[['subrgn', 'srname']] 
         
            try:
                with engine.connect() as conn:
                    trans = conn.begin()
                    conn.execute(text("truncate table subregion cascade;"))  
                    # result = conn.execute(text("SELECT COUNT(*) FROM plant;"))
                   
                    trans.commit() 
                df.to_sql('subregion', con=engine, if_exists='append', index=False)
                print('Success inserting subregion data.')
                return {"success": True, "message": "Data successfully inserted into the subregion table."}
            except Exception as e:
                print('Error inserting nerc data.', e)
                return {"error": str(e)}
              
    except Exception as e:
        logger.error(f"Error while processing R API data: {e}", exc_info=True)
        return {"error": str(e)}
