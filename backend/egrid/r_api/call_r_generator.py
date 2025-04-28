# File to communicate with the R API
import requests  
import logging
import pandas as pd  
from sqlalchemy import text 
from .utils import record_insert_update

logger = logging.getLogger('egrid')
   
def populate_generator_data(engine=None, api_url=None, year=None):
    print("Starting script to populate generator data for year ", year)

    try:
        response = requests.get(f"{api_url}{year}/generator")
        data = response.json()  

        if response.status_code == 200 and data.get('success'):
            gen_data = data.get('data', [])
            df = pd.DataFrame(gen_data)

            year = df['year'].unique()[0] 

            # Cast columns to appropriate types
            cast_to_float = ['namepcap', 'cfact', 'genntan', 'genntoz']
            cast_to_int = ['orispl', 'numblr', 'genyronl', 'genyrret', 'year']
 
            for col in cast_to_int:
                df[col] = pd.to_numeric(df[col], errors='coerce').astype("Int64")

            for col in cast_to_float:
                df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)
 
            # print('df', df.head()) # for debugging
            gen_df = df[['genid', 'orispl']] 
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

                    conn.execute(text("""
                        insert into generator (genid, orispl) 
                        select genid, orispl 
                        from generator_temp
                        on conflict (genid, orispl) do update
                        set
                            orispl = excluded.orispl, 
                            genid = excluded.genid;
                    """))  

                    # conn.execute(text("""
                    #     insert into generation (
                    #         genid, orispl, year, numblr,
                    #         genstat, prmvr, fuelg1, namepcap ,cfact,
                    #         genntan, genntoz, genersrc, genyronl, genyrret
                    #     ) select genid, orispl, year, numblr,
                    #         genstat, prmvr, fuelg1, namepcap ,cfact,
                    #         genntan, genntoz, genersrc, genyronl, genyrret
                    #     from generator_temp
                    #     on conflict (orispl, genid, year) do update
                    #     set
                    #         numblr = excluded.numblr,
                    #         genstat = excluded.genstat, 
                    #         prmvr = excluded.prmvr,
                    #         fuelg1 = excluded.fuelg1,
                    #         namepcap = excluded.namepcap,
                    #         cfact = excluded.cfact, 
                    #         genntan = excluded.genntan,
                    #         genntoz = excluded.genntoz, 
                    #         genersrc = excluded.genersrc,
                    #         genyronl = excluded.genyronl,
                    #         genyrret = excluded.genyrret;
                    # """))
  
                    try: 
                        sql = record_insert_update("generation", generation_df, unique_field=['orispl', 'genid'])
                        conn.execute(text(sql))
                        print("Successfully upserted: generation")
                    except Exception as e: 
                        print(f"Error processing generation: {e}")


                    # conn.execute(text("truncate table generator_temp;"))
                    conn.execute(text("drop table generator_temp;"))
                    conn.execute(text("drop table generation_temp;"))
 
                    trans.commit() 
 
                print('Success populating generator data.')  
                  
            except Exception as e:
                print('Error populating generator data.', e)
                return {"error": str(e)}  

            return {"success": True, "message": "Data successfully inserted into the Generator table."}
        else:
            return {"error": f"Failed to connect to R API with status code {response.status_code}"}
    
    except Exception as e:
        return {"error": str(e)}