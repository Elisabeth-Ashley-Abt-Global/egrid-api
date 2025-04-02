from egrid.models import Plant
import requests
import logging
import pandas as pd 
from sqlalchemy import create_engine, text 
from django.conf import settings
logger = logging.getLogger('egrid')

def sanitize_numeric(value):
    try:
        return float(value)  # Convert to a float or int
    except (ValueError, TypeError):
        return None  # Return None for invalid values

def call_r_plant():

    engine = create_engine(
    f"postgresql://{settings.DATABASES['default']['USER']}:{settings.DATABASES['default']['PASSWORD']}@"
    f"{settings.DATABASES['default']['HOST']}:{settings.DATABASES['default']['PORT']}/"
    f"{settings.DATABASES['default']['NAME']}"
    )   

    try:
        response = requests.get("http://127.0.0.1:8001/plant")
        data = response.json() 
     
        if response.status_code == 200 and data.get('success'):
            plant_data = data.get('data', [])
            df = pd.DataFrame(plant_data)
        
            df = df[['pstatabb', 'fipsst', 'orispl', 'utlsrvid', 'bacode', 'nerc', 'fipscnty', 'lat', 'lon', 'numunt', 'numgen', 'plprmfl', 'plfuelct', 'oprcode', 'sector', 'pname', 'coalflag','sequnt']] 
         
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

 