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
            gen_df = pd.DataFrame(gen_data)
            # print('df', df.head()) # for debugging
            gen_df = gen_df[['seqgen', 'genid', 'orispl']] 
            gen_df = gen_df.copy()
            gen_df.replace({"--": pd.NA, "N/A": pd.NA, "": pd.NA}, inplace=True) 
            
            # Cast columns to appropriate types
            cast_to_float = ['seqgen']
            cast_to_int = ['orispl']

            for col in cast_to_int:
                gen_df[col] = pd.to_numeric(gen_df[col], errors='coerce').astype("Int64")

            for col in cast_to_float:
                gen_df[col] = pd.to_numeric(gen_df[col], errors='coerce').astype(float)
 
            try: 
                gen_df.to_sql('generator_temp', con=engine, if_exists='replace', index=False)


                with engine.connect() as conn:
                    trans = conn.begin()

                    gen_cnt = conn.execute(text("select count(*) from generator;")).scalar()

                    if gen_cnt == 0:
                                
                        conn.execute(text("""
                            insert into generator (
                                seqgen, genid, orispl
                            ) select seqgen, genid, orispl from generator_temp;
                        """)) 

                    else:
                        conn.execute(text("""
                            update generator 
                            set seqgen = generator_temp.seqgen, 
                            genid = generator_temp.genid
                            from generator_temp  
                            where generator.orispl = generator_temp.orispl 
                                and generator.genid = generator_temp.genid;
                        """))


                    conn.execute(text("truncate table generator_temp;"))
                    conn.execute(text("drop table generator_temp;"))
                    trans.commit() 

                gen_df.to_sql('generator', con=engine, if_exists='append', index=False)
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