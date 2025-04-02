from egrid.models import Plant
import requests
import logging
import pandas as pd 
from sqlalchemy import create_engine, text 
from django.conf import settings
logger = logging.getLogger('egrid')
  
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
            print(df['utlsrvid'].dtype)
            df = df[['pstatabb', 'fipsst', 'orispl', 'utlsrvid', 'bacode', 'nerc', 'fipscnty', 'lat', 'lon', 'numunt', 'numgen', 'plprmfl', 'plfuelct', 'oprcode', 'sector', 'pname', 'coalflag','sequnt']] 
            df = df.copy()
            df.replace({"--": pd.NA, "N/A": pd.NA, "": pd.NA}, inplace=True) # replace placeholders else you'll encounter  invalid input syntax for type double precision
             
            columns_to_cast = [ 'orispl', 'utlsrvid', 'fipscnty',  'numunt', 'numgen',  'oprcode' ]

            #'lat', 'lon',
            for col in columns_to_cast:
                df[col] = df[col].fillna(0).astype(int)

            try:
                # storing the data in a temporary upload table 
                df.to_sql('plant_temp', con=engine, if_exists='append', index=False)

                with engine.connect() as conn:
                    trans = conn.begin()
                    conn.execute(text("""update plant set pstatabb = plant_temp.pstatabb, 
                    fipsst = plant_temp.fipsst, utlsrvid = plant_temp.utlsrvid,
                    bacode = plant_temp.bacode, nerc = plant_temp.nerc, fipscnty = plant_temp.fipscnty, 
                    lat = plant_temp.lat, lon = plant_temp.lon, numunt = plant_temp.numunt, 
                    numgen = plant_temp.numgen, plprmfl = plant_temp.plprmfl, plfuelct = plant_temp.plfuelct, 
                    oprcode = plant_temp.oprcode, sector = plant_temp.sector, pname = plant_temp.pname, 
                    coalflag = plant_temp.coalflag, sequnt = plant_temp.sequnt 
                    from plant_temp  
                    where plant.orispl = plant_temp.orispl;
                    """))

                    conn.execute(text("truncate table plant_temp;"))

                    trans.commit() 
  
                print('Success inserting plant data.')
                return {"success": True, "message": "Data successfully inserted into the Generator table."}
            except Exception as e:
                print('Error inserting plant data.', e)
                return {"error": str(e)}
              
    except Exception as e:
        logger.error(f"Error while processing R API data: {e}", exc_info=True)
        return {"error": str(e)}

 