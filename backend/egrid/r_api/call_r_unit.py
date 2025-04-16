# File to communicate with the R API
import requests  
import logging
import pandas as pd  
from sqlalchemy import text 
from .utils import update_from_temp_table, build_insert_from_temp_sql 

logger = logging.getLogger('egrid')

def populate_unit_data(engine=None, api_url=None, year=None): 
    print('populate_unit_data')
    logger.debug("*populate_unit_data")

    try:
        response = requests.get(f"{api_url}{year}/unit")
        data = response.json() 
        # print('data', data)

        if response.status_code == 200 and data.get('success'):
            unit_data = data.get('data', [])
            df = pd.DataFrame(unit_data)
        
            cast_to_int = ['year', 'orispl', 'numgen', 'untyronl', 'sequnt']

            # Define the new columns to type cast (2023+ data)
            new_cols = ['stackht'] # TG: this is in UnitUnadjustedValues

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
            print('year ', year)    

            # create tables
            # Unit
            unit_df = df[['sequnt', 'orispl', 'unitid', 'prmvr', 'capdflag', 
                        'prgcode', 'botfirty', 'numgen']].copy()

            # UnitUnadjustedValues
            # 'untopst'
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

                    # count to see if table is empty
                    unit_cnt = conn.execute(text("""
                            SELECT COUNT(*)
                            FROM unit_temp ut
                            WHERE EXISTS (
                                SELECT 1 FROM unit u
                                WHERE u.orispl = ut.orispl
                                AND u.unitid = ut.unitid
                                AND u.prmvr = ut.prmvr
                            )
                        """)).scalar()
                    
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
                            )
                            select 
                                ut.sequnt, ut.orispl, ut.unitid, ut.prmvr, ut.capdflag, 
                                ut.prgcode, ut.botfirty, ut.numgen
                            from unit_temp ut
                            where not exists (
                                select 1 
                                from unit u
                                where u.orispl = ut.orispl
                                and u.unitid = ut.unitid
                                and u.prmvr = ut.prmvr
                            ); 
                        """))  
                        print('inserted unit data')
                    else:
                        conn.execute(text("""
                            update unit
                            set 
                                sequnt = unt.sequnt,
                                orispl = unt.orispl,
                                unitid = unt.unitid,
                                prmvr = unt.prmvr,
                                capdflag = unt.capdflag,
                                prgcode = unt.prgcode,
                                botfirty = unt.botfirty,
                                numgen = unt.numgen
                            from unit_temp unt
                            where unit.orispl = unt.orispl
                            and unit.unitid = unt.unitid
                            and unit.prmvr = unt.prmvr;
                        """))  
                        print('updated unit data')

#fuelu1,            
                    # if unitunadjustedvalues_cnt == 0:
                    #     conn.execute(text("""
                    #         insert into unit_unadjusted_values (
                    #             orispl, unitid, prmvr,
                    #             hrsop, htian, htioz, noxan, noxoz, 
                    #             so2an, co2an, hgan, htiansrc, 
                    #             htiozsrc, noxansrc, noxozsrc, so2src, 
                    #             co2src, hgsrc, so2ctldv, noxctldv, 
                    #             hgctldv, untyronl, stackht
                    #         ) select  orispl, unitid, prmvr,  
                    #             hrsop, htian, htioz, noxan, noxoz, 
                    #             so2an, co2an, hgan, htiansrc, 
                    #             htiozsrc, noxansrc, noxozsrc, so2src, 
                    #             co2src, hgsrc, so2ctldv, noxctldv, 
                    #             hgctldv, untyronl, stackht
                    #         from unit_temp;
                    #     """))  
                    # else:
                    #     conn.execute(text("""
                    #         update unit_unadjusted_values
                    #         set orispl = unt.orispl, 
                    #             unitid = unt.unitid, 
                    #             prmvr = unt.prmvr,
                    #             untopst = unt.untopst, 
                    #             fuelu1 = unt.fuelu1,
                    #             hrsop = unt.hrsop, 
                    #             htian = unt.htian, 
                    #             htioz = unt.htioz, 
                    #             noxan = unt.noxan, 
                    #             noxoz = unt.noxoz, 
                    #             so2an = unt.so2an, 
                    #             co2an = unt.co2an, 
                    #             hgan = unt.hgan, 
                    #             htiansrc = unt.htiansrc, 
                    #             htiozsrc = unt.htiozsrc, 
                    #             noxansrc = unt.noxansrc, 
                    #             noxozsrc = unt.noxozsrc, 
                    #             so2src = unt.so2src, 
                    #             co2src = unt.co2src, 
                    #             hgsrc = unt.hgsrc, 
                    #             so2ctldv = unt.so2ctldv, 
                    #             noxctldv = unt.noxctldv, 
                    #             hgctldv = unt.hgctldv, 
                    #             untyronl = unt.untyronl, 
                    #             stackht = unt.stackht
                    #         from unit_temp unt
                    #         where orispl = unt.orispl and
                    #             unitid = unt.unitid and
                    #             prmvr = unt.prmvr;
                    #     """))  

                    # drop temp tables
                    # conn.execute(text("drop table unit_temp;"))
                    # conn.execute(text("drop table unit_unadjusted_values_temp;")) 
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

                   

                
