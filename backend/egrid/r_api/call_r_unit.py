# File to communicate with the R API
import requests  
import logging
import pandas as pd  
from sqlalchemy import text 
from .utils import update_from_temp_table, build_insert_from_temp_sql 

logger = logging.getLogger('egrid')

def populate_unit_data(engine=None, api_url=None): 
    print('populate_unit_data')
    logger.debug("*populate_unit_data")

    try:
        response = requests.get(f"{api_url}unit")
        data = response.json() 

        if response.status_code == 200 and data.get('success'):
            unit_data = data.get('data', [])
            df = pd.DataFrame(unit_data)
        
            cast_to_int = ['year', 'orispl', 'numgen', 'untyronl', 'sequnt']

            # Define the new columns to type cast (2023+ data)
            new_cols = ['stackht'] # TG: this is in UnitUnadjustedValues

            cast_to_float = ['hrsop', 'htian', 'htioz', 'noxan', 'noxoz', 
                             'so2an', 'co2an', 'hgan', 'stackht']
            
            for col in cast_to_int:
                df[col] = pd.to_numeric(df[col], errors='coerce').astype("Int64")

            for col in cast_to_float:
                df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)

            year = df['year'].unique()[0] 
            print('year ', year)    

            # create tables
            # Unit
            unit_df = df[['sequnt', 'orispl', 'unitid', 'prmvr', 'capdflag', 
                        'prgcode', 'botfirty', 'numgen']].copy()

            # UnitUnadjustedValues
            try: 
                unitunadjustedvalues_df = df[['year', 'orispl', 'unitid', 'prmvr', 'untopst', 'fuelu1',
                                              'hrsop', 'htian', 'htioz', 'noxan', 'noxoz', 
                                              'so2an', 'co2an', 'hgan', 'htiansrc', 
                                              'htiozsrc', 'noxansrc', 'noxozsrc', 'so2src', 
                                              'co2src', 'hgsrc', 'so2ctldv', 'noxctldv', 
                                              'hgctldv', 'untyronl', 'stackht']].copy()
                unitunadjustedvalues_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in UnitUnadjustedValues dataframe')

            try:
                # build temp tables, replace will replace the table if it already exists
                unit_df.to_sql('unit_temp', con=engine, if_exists='replace', index=False) 
                unitunadjustedvalues_df.to_sql('unit_unadjusted_values_temp', con=engine, if_exists='replace', index=False)

                with engine.connect() as conn:
                    trans = conn.begin()

                    # count to see if table is empty
                    unit_cnt = conn.execute(text("select count(*) from unit;")).scalar()

                    unitunadjustedvalues_cnt = conn.execute(
                        text("select count(*) from unit_unadjusted_values where year = :year"),
                        {"year": int(year)}
                    ).scalar()  

                    # check count to insert or update the table
                    if unit_cnt == 0:
                        conn.execute(text("""
                            insert into unit (
                                sequnt, orispl, unitid, prmvr, capdflag, 
                                prgcode, botfirty, numgen
                            ) select sequnt, orispl, unitid, prmvr capdflag, 
                                prgcode, botfirty, numgen
                            from unit_temp;
                        """))  
                    else:
                        conn.execute(text("""
                            update unit
                            set sequnt = unt.sequnt
                                orispl = unt.orispl, 
                                unitid = unt.unitid, 
                                prmvr = unt.prmvr
                                capdflag = unt.capdflag, 
                                prgcode = unt.prgcode, 
                                botfirty = unt.botfirty, 
                                numgen = unt.numgen
                            from unit_temp unt
                            where unit.orispl = unt.orispl and
                                unit.unitid = unt.unitid and
                                unit.prmvr = unt.prmvr;
                        """))  

                    if unitunadjustedvalues_cnt == 0:
                        conn.execute(text("""
                            insert into unit (
                                year, orispl, unitid, prmvr, untopst, fuelu1,
                                hrsop, htian, htioz, noxan, noxoz, 
                                so2an, co2an, hgan, htiansrc, 
                                htiozsrc, noxansrc, noxozsrc, so2src, 
                                co2src, hgsrc, so2ctldv, noxctldv, 
                                hgctldv, untyronl, stackht
                            ) select year, orispl, unitid, prmvr, untopst, fuelu1,
                                hrsop, htian, htioz, noxan, noxoz, 
                                so2an, co2an, hgan, htiansrc, 
                                htiozsrc, noxansrc, noxozsrc, so2src, 
                                co2src, hgsrc, so2ctldv, noxctldv, 
                                hgctldv, untyronl, stackht
                            from unit_temp;
                        """))  
                    else:
                        conn.execute(text("""
                            update unit
                            set year = unt.year, 
                                orispl = unt.orispl, 
                                unitid = unt.unitid, 
                                prmvr = unt.prmvr,
                                untopst = unt.untopst, 
                                fuelu1 = unt.fuelu1,
                                hrsop = unt.hrsop, 
                                htian = unt.htian, 
                                htioz = unt.htioz, 
                                noxan = unt.noxan, 
                                noxoz = unt.noxoz, 
                                so2an = unt.so2an, 
                                co2an = unt.co2an, 
                                hgan = unt.hgan, 
                                htiansrc = unt.htiansrc, 
                                htiozsrc = unt.htiozsrc, 
                                noxansrc = unt.noxansrc, 
                                noxozsrc = unt.noxozsrc, 
                                so2src = unt.so2src, 
                                co2src = unt.co2src, 
                                hgsrc = unt.hgsrc, 
                                so2ctldv = unt.so2ctldv, 
                                noxctldv = unt.noxctldv, 
                                hgctldv = unt.hgctldv, 
                                untyronl = unt.untyronl, 
                                stackht = unt.stackht
                            from unit_temp unt
                            where unit.orispl = unt.orispl and
                                unit.unitid = unt.unitid and
                                unit.prmvr = unt.prmvr;
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

                   

                
