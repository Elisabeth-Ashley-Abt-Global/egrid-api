# File to communicate with the R API
import requests  
import logging
import pandas as pd  
from sqlalchemy import text 

logger = logging.getLogger('egrid')

def populate_unit_data(engine=None, api_url=None, year=None): 
    print("Starting script to populate unit data for year ", year)

    try:
        response = requests.get(f"{api_url}{year}/unit")
        data = response.json() 
        #print('data', data)

        if response.status_code == 200 and data.get('success'):
            unit_data = data.get('data', [])
            df = pd.DataFrame(unit_data)
        
            cast_to_int = ['year', 'orispl', 'numgen', 'untyronl']

            # Define the new columns to type cast (2023+ data)
            new_cols = ['stackht'] 

            cast_to_float = ['hrsop', 'htian', 'htioz', 'noxan', 'noxoz', 
                             'so2an', 'co2an', 'hgan', 'stackht']
            
            # Cast columns to appropriate types, check if in new columns
            for col in cast_to_int:
                try:
                    if year >= 2023:
                        df[col] = pd.to_numeric(df[col], errors='coerce').astype("Int64")
                    else:
                        if col not in new_cols: 
                            df[col] = pd.to_numeric(df[col], errors='coerce').astype("Int64")

                except Exception as e:
                    print('Error converting column to Int64:', col, e)

            for col in cast_to_float:
                try:
                    if year >= 2023: # Double check this
                        df[col] = pd.to_numeric(df[col], errors='coerce').astype("float")
                    else:
                        if col not in new_cols: 
                            df[col] = pd.to_numeric(df[col], errors='coerce').astype("float")
                            
                except Exception as e:
                    print('Error converting column to float:', col, e)

            year = df['year'].unique()[0] 
              

            # create tables
            # Unit
            unit_df = df[['orispl', 'unitid', 'prmvr', 'capdflag', 
                        'prgcode', 'botfirty', 'numgen']].copy()

            # UnitUnadjustedValues
            try: 
                unitunadjustedvalues_df = df[['year', 'orispl', 'unitid', 'prmvr', 'untopst', 'fuelu1',
                                              'hrsop', 'htian', 'htioz', 'noxan', 'noxoz', 
                                              'so2an', 'co2an', 'hgan', 'htiansrc', 
                                              'htiozsrc', 'noxansrc', 'noxozsrc', 'so2src', 
                                              'co2src', 'hgsrc', 'so2ctldv', 'noxctldv', 
                                              'hgctldv', 'untyronl']].copy()
                if year >= 2023: 
                    unitunadjustedvalues_df['stackht'] = df['stackht']

                unitunadjustedvalues_df.copy()
                unitunadjustedvalues_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in UnitUnadjustedValues dataframe')
            
            try:
                # build temp tables, replace will replace the table if it already exists
                unit_df.to_sql('unit_temp', con=engine, if_exists='replace', index=False) 
                unitunadjustedvalues_df.to_sql('unit_unadjusted_values_temp', con=engine, if_exists='replace', index=False)

                with engine.connect() as conn:
                    trans = conn.begin()

                    conn.execute(text("""
                        insert into unit (
                        orispl, unitid, prmvr, capdflag, 
                        prgcode, botfirty, numgen
                        )
                        select 
                            orispl, unitid, prmvr, capdflag, 
                            prgcode, botfirty, numgen
                        from unit_temp 
                        on conflict (orispl, unitid, prmvr) do update
                        set
                            capdflag = excluded.capdflag, 
                            prgcode = excluded.prgcode, 
                            botfirty = excluded.prgcode, 
                            numgen = excluded.numgen;
                    """))  

                    conn.execute(text(""" 
                        insert into unit_unadjusted_values (
                            orispl, unitid, prmvr,
                            hrsop, htian, htioz, noxan, noxoz, 
                            so2an, co2an, hgan, htiansrc, 
                            htiozsrc, noxansrc, noxozsrc, so2src, 
                            co2src, hgsrc, so2ctldv, noxctldv, 
                            hgctldv, untyronl, stackht
                        ) 
                        select  
                            orispl, unitid, prmvr,  
                            hrsop, htian, htioz, noxan, noxoz, 
                            so2an, co2an, hgan, htiansrc, 
                            htiozsrc, noxansrc, noxozsrc, so2src, 
                            co2src, hgsrc, so2ctldv, noxctldv, 
                            hgctldv, untyronl, stackht
                        from unit_unadjusted_values_temp   
                        on conflict (orispl, unitid, prmvr, year) do update
                        set 
                            untopst = excluded.untopst, 
                            fuelu1 = excluded.fuelu1,
                            hrsop = excluded.hrsop, 
                            htian = excluded.htian, 
                            htioz = excluded.htioz, 
                            noxan = excluded.noxan, 
                            noxoz = excluded.noxoz, 
                            so2an = excluded.so2an, 
                            co2an = excluded.co2an, 
                            hgan = excluded.hgan, 
                            htiansrc = excluded.htiansrc, 
                            htiozsrc = excluded.htiozsrc, 
                            noxansrc = excluded.noxansrc, 
                            noxozsrc = excluded.noxozsrc, 
                            so2src = excluded.so2src, 
                            co2src = excluded.co2src, 
                            hgsrc = excluded.hgsrc, 
                            so2ctldv = excluded.so2ctldv, 
                            noxctldv = excluded.noxctldv, 
                            hgctldv = excluded.hgctldv, 
                            untyronl = excluded.untyronl, 
                            stackht = excluded.stackht           
                    """)) 

                    # drop temp tables
                    conn.execute(text("drop table unit_temp;"))
                    conn.execute(text("drop table unit_unadjusted_values_temp;")) 
                    trans.commit() 

                print('Success populating unit data.')  
                  
            except Exception as e:
                print('Error populating unit data.', e)
                return {"error": str(e)}  

            return {"success": True, "message": "Data successfully inserted into the Unit table."}
        else:
            return {"error": f"Failed to connect to R API with status code {response.status_code}"}
    
    except Exception as e:
        return {"error": str(e)}                       

                   

                
