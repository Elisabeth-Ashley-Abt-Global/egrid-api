# File to communicate with the R API
import requests  
import logging
import pandas as pd  
from sqlalchemy import text 
from .utils import record_insert_update 

logger = logging.getLogger('egrid')
   
def populate_generator_data(engine=None, api_url=None, year=None):
    print('populate_generator_data')
    logger.debug("*populate_generator_data")
     
    try:
        response = requests.get(f"{api_url}{year}/generator")
        data = response.json()  

        if response.status_code == 200 and data.get('success'):
            gen_data = data.get('data', [])
            df = pd.DataFrame(gen_data)

            year = df['year'].unique()[0] 
            print('year ', year)
            # Cast columns to appropriate types
            cast_to_float = ['namepcap', 'cfact', 'genntan', 'genntoz']
            cast_to_int = ['orispl', 'numblr', 'genyronl', 'genyrret', 'year']
 
            for col in cast_to_int:
                df[col] = pd.to_numeric(df[col], errors='coerce').astype("Int64")

            for col in cast_to_float:
                df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)
 
            # print('df', df.head()) # for debugging
            gen_df = df[['orispl', 'genid']] 
            gen_df = df.copy()
            gen_df.replace({"--": pd.NA, "N/A": pd.NA, "": pd.NA}, inplace=True) 

            generation_df = df[['genid','orispl','year','numblr',
                                'genstat', 'prmvr', 'fuelg1', 'namepcap' ,'cfact',
                                'genntan', 'genntoz', 'genersrc', 'genyronl', 'genyrret']]
            
            tables = ["generation"]
            
            df_map = {
                "generation": generation_df,
            }

            try: 
                gen_df.to_sql('generator_temp', con=engine, if_exists='replace', index=False) 
                generation_df.to_sql('generation_temp', con=engine, if_exists='replace', index=False)

                with engine.connect() as conn:
                    trans = conn.begin()

                    gen_cnt = conn.execute(text("select count(*) from generator;")).scalar()
                    generation_cnt = conn.execute(
                        text("select count(*) from generation where year = :year"),
                        {"year": year}
                    ).scalar() 

                    if gen_cnt == 0:   
                        conn.execute(text("""
                            insert into generator (
                                genid, orispl
                            ) select genid, orispl from generator_temp;
                        """))  
                    else:
                        conn.execute(text("""
                            update generator 
                            genid = gt.genid
                            from generator_temp gt 
                            where generator.orispl = gt.orispl 
                                and generator.genid = gt.genid;
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
                            set genid = gt.genid,
                            year = gt.year, 
                            numblr = generator_temp.numblr,
                            genstat = gt.genstat, 
                            prmvr = gt.prmvr,
                            fuelg1 = gt.fuelg1,
                            namepcap = gt.namepcap,
                            cfact = gt.cfact, 
                            genntan = gt.genntan,
                            genntoz = gt.genntoz, 
                            genersrc = gt.genersrc,
                            genyronl = gt.genyronl,
                            genyrret = gt.genyrret
                            from generator_temp gt
                            where generation.orispl = gt.orispl 
                                and generation.genid = gt.genid
                                and generation.year = gt.year;
                        """))
  
                    # conn.execute(text("truncate table generator_temp;"))
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