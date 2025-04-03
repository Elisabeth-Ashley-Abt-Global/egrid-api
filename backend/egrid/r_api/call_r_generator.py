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

            # Cast columns to appropriate types
            cast_to_float = ['seqgen', 'namepcap', 'cfact', 'genntan', 'genntoz']
            cast_to_int = ['orispl', 'numblr', 'genyronl', 'genyrret', 'year']
 
            for col in cast_to_int:
                df[col] = pd.to_numeric(df[col], errors='coerce').astype("Int64")

            for col in cast_to_float:
                df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)


            # print('df', df.head()) # for debugging
            gen_df = df[['seqgen', 'genid', 'orispl']] 
            gen_df = df.copy()
            gen_df.replace({"--": pd.NA, "N/A": pd.NA, "": pd.NA}, inplace=True) 

            generation_df = df[['genid','orispl','year','numblr',
                                    'genstat', 'prmvr', 'fuelg1', 'namepcap' ,'cfact',
                                    'genntan', 'genntoz', 'genersrc', 'genyronl', 'genyrret']]
             
 
            try: 
                gen_df.to_sql('generator_temp', con=engine, if_exists='replace', index=False) 
                generation_df.to_sql('generation_temp', con=engine, if_exists='replace', index=False)

                with engine.connect() as conn:
                    trans = conn.begin()

                    gen_cnt = conn.execute(text("select count(*) from generator;")).scalar()
                    generation_cnt = conn.execute(text("select count(*) from generation;")).scalar()
 
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

                    if generation_cnt == 0:
                        conn.execute(text("""
                            insert into generation (
                              genid, orispl, year, numblr,
                                genstat, prmvr, fuelg1, namepcap ,cfact,
                                genntan, genntoz, genersrc, genyronl, genyrret
                            ) select genid, orispl, year, numblr,
                                genstat, prmvr, fuelg1, namepcap ,cfact,
                                genntan, genntoz, genersrc, genyronl, genyrret
                            from generator_temp;
                        """))
                    else:   
                        conn.execute(text("""  
                            update generation 
                            set genid = generator_temp.genid,
                            year = generator_temp.year, 
                            numblr = generator_temp.numblr,
                            genstat = generator_temp.genstat, 
                            prmvr = generator_temp.prmvr,
                            fuelg1 = generator_temp.fuelg1,
                            namepcap = generator_temp.namepcap,
                            cfact = generator_temp.cfact, 
                            genntan = generator_temp.genntan,
                            genntoz = generator_temp.genntoz, 
                            genersrc = generator_temp.genersrc,
                            genyronl = generator_temp.genyronl,
                            genyrret = generator_temp.genyrret
                            from generator_temp  
                            where generation.orispl = generator_temp.orispl 
                                and generation.genid = generator_temp.genid;
                        """))
  
                    conn.execute(text("truncate table generator_temp cascade;"))
                    conn.execute(text("drop table generator_temp;"))
                    conn.execute(text("drop table generation_temp;"))
 
                    trans.commit() 
 
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