# File to communicate with the R API
import requests  
import logging
import pandas as pd  
from sqlalchemy import text 
from .utils import update_from_temp_table, build_insert_from_temp_sql 


logger = logging.getLogger('egrid')
 
def populate_nerc_data(engine=None, api_url=None): 
    print('populate_nerc_data')
    logger.debug("*populate_nerc_data")

    try:
        response = requests.get(f"{api_url}nerc")
        data = response.json() 
        
        if response.status_code == 200 and data.get('success'):
            nerc_data = data.get('data', [])
            df = pd.DataFrame(nerc_data)
        
            cast_to_int = ['year']
            cast_to_float = ['nrnamepcap', 'nrhtian', 'nrhtioz', 'nrhtiant', 
                             'nrhtiozt', 'nrngenan', 'nrngenoz', 'nrngennb', 
                             'nrnoxan', 'nrnoxoz', 'nrso2an', 'nrco2an', 
                             'nrch4an', 'nrn2oan', 'nrco2eqa', 'nrnoxrta',
                             'nrnoxrto', 'nrso2rta', 'nrco2rta', 'nrch4rta', 
                             'nrn2orta', 'nrc2erta', 'nrnoxra', 'nrnoxro',
                             'nrso2ra', 'nrco2ra', 'nrch4ra', 'nrn2ora', 
                             'nrc2era', 'nrnoxcrt', 'nrnoxcro', 'nrso2crt', 
                             'nrco2crt', 'nrch4crt', 'nrn2ocrt', 'nrc2ecrt', 
                             'nrcnoxrt', 'nronoxrt', 'nrgnoxrt', 'nrfsnxrt', 
                             'nrcnxort', 'nronxort', 'nrgnxort', 'nrfsnort', 
                             'nrcso2rt', 'nroso2rt', 'nrgso2rt', 'nrfss2rt', 
                             'nrcco2rt', 'nroco2rt', 'nrgco2rt', 'nrfsc2rt', 
                             'nrcch4rt', 'nroch4rt', 'nrgch4rt', 'nrfch4rt', 
                             'nrcn2ort', 'nron2ort', 'nrgn2ort', 'nrfn2ort', 
                             'nrcc2ert', 'nroc2ert', 'nrgc2ert', 'nrfsc2ert',
                             'nrcnoxr', 'nronoxr', 'nrgnoxr', 'nrfsnxr',
                             'nrcnxor', 'nronxor', 'nrgnxor', 'nrfsnor',
                             'nrcso2r', 'nroso2r', 'nrgso2r', 'nrfss2r', 
                             'nrcco2r', 'nroco2r', 'nrgco2r', 'nrfsc2r',
                             'nrcch4r', 'nroch4r', 'nrgch4r', 'nrfch4r',
                             'nrcn2or', 'nron2or', 'nrgn2or', 'nrfn2or', 
                             'nrcc2er', 'nroc2er', 'nrgc2er',  'nrfsc2er', 
                             'nrgenacl', 'nrgenaol', 'nrgenaso', 'nrgenagt',
                             'nrgenaof', 'nrgenaop', 'nrgenatn', 'nrgenatr', 
                             'nrgenato', 'nrgenath', 'nrgenacy', 'nrgenacn',
                             'nrgenaco', 'nrgenags', 'nrgenanc', 'nrgenahy',
                             'nrgenabm', 'nrgenawi', 'nrnbnox', 'nrnbnxo',
                             'nrnbso2', 'nrnbco2', 'nrnbch4', 'nrnbn2o',   
                             'nrnbc2e', 'nrnbgncl', 'nrnbgnol', 'nrnbgngs',  
                             'nrnbgnnc', 'nrnbgnhy', 'nrnbgnbm', 'nrnbgnwi',  
                             'nrnbgnso', 'nrnbgngt', 'nrnbgnof', 'nrnbgnop',  
                             'nrnbclpr', 'nrnbolpr', 'nrnbgspr', 'nrnbncpr',  
                             'nrnbhypr', 'nrnbbmpr', 'nrnbwipr', 'nrnbsopr',  
                             'nrnbgtpr', 'nrnbofpr', 'nrnboppr', 'nrclpr',
                             'nrolpr', 'nrgspr', 'nrncpr', 'nrhypr', 
                             'nrbmpr', 'nrwipr', 'nrsopr', 'nrgtpr', 
                             'nrofpr', 'nroppr', 'nrtnpr', 'nrtrpr',
                             'nrtopr', 'nrthpr', 'nrcypr', 'nrcnpr', 
                             'nrcopr']

            for col in cast_to_int:
                df[col] = pd.to_numeric(df[col], errors='coerce').astype(int)

            for col in cast_to_float:
                df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)

            year = df['year'].unique()[0] 
            print('year ', year)

            nerc_df = df[['nerc', 'nercname', 'nrnamepcap']].copy() 

            # NercAdjustedValues
            try: 
                nercadjustedvalues_df = df[['nerc', 'nrhtian', 'nrhtioz', 'nrhtiant', 
                                            'nrhtiozt', 'nrngenan', 'nrngenoz', 'nrngennb', 
                                            'nrnoxan', 'nrnoxoz', 'nrso2an', 'nrco2an', 
                                            'nrch4an', 'nrn2oan', 'nrco2eqa', 'nrhgan', 'year']].copy()
                nercadjustedvalues_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in NercAdjustedValues dataframe')

            # NercEmissionRate
            try: 
                nercemissionrate_df = df[['nerc', 'nrnoxrta', 'nrnoxrto', 'nrso2rta', 
                                        'nrco2rta', 'nrch4rta', 'nrn2orta', 'nrc2erta', 
                                        'nrhgrta', 'nrnoxra', 'nrnoxro', 'nrso2ra',  
                                        'nrco2ra', 'nrch4ra', 'nrn2ora', 'nrc2era',  
                                        'nrhgra', 'nrnoxcrt', 'nrnoxcro', 'nrso2crt', 
                                        'nrco2crt', 'nrch4crt', 'nrn2ocrt', 'nrc2ecrt', 
                                        'nrhgcrt', 'year']].copy()
                nercemissionrate_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in NercEmissionRate dataframe')

            # NercFuelTypeEmissionRate
            try: 
                nercfueltypeemissionrate_df = df[['nerc', 'nrcnoxrt', 'nronoxrt', 'nrgnoxrt', 'nrfsnxrt', 
                                                'nrcnxort', 'nronxort', 'nrgnxort', 'nrfsnort', 
                                                'nrcso2rt', 'nroso2rt', 'nrgso2rt', 'nrfss2rt', 
                                                'nrcco2rt', 'nroco2rt', 'nrgco2rt', 'nrfsc2rt', 
                                                'nrcch4rt', 'nroch4rt', 'nrgch4rt', 'nrfch4rt', 
                                                'nrcn2ort', 'nron2ort', 'nrgn2ort', 'nrfn2ort', 
                                                'nrcc2ert', 'nroc2ert', 'nrgc2ert', 'nrfsc2ert',
                                                'nrchgrt', 'nrfshgrt', 'nrcnoxr', 'nronoxr', 
                                                'nrgnoxr', 'nrfsnxr', 'nrcnxor', 'nronxor', 
                                                'nrgnxor', 'nrfsnor', 'nrcso2r', 'nroso2r', 
                                                'nrgso2r', 'nrfss2r', 'nrcco2r', 'nroco2r', 
                                                'nrgco2r', 'nrfsc2r', 'nrcch4r', 'nroch4r', 
                                                'nrgch4r', 'nrfch4r', 'nrcn2or', 'nron2or', 
                                                'nrgn2or', 'nrfn2or', 'nrcc2er', 'nroc2er', 
                                                'nrgc2er',  'nrfsc2er', 'nrchgr', 'nrfshgr', 'year']].copy()
                nercfueltypeemissionrate_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in NercFuelTypeEmissionRate dataframe')

            # NercFuelTypeGeneration
            try: 
                nercfueltypegeneration_df = df[['nerc', 'nrgenacl', 'nrgenaol', 'nrgenaso', 'nrgenagt',
                                                'nrgenaof', 'nrgenaop', 'nrgenatn', 'nrgenatr', 
                                                'nrgenato', 'nrgenath', 'nrgenacy', 'nrgenacn',
                                                'nrgenaco', 'nrgenags', 'nrgenanc', 'nrgenahy',
                                                'nrgenabm', 'nrgenawi', 'year']].copy()
                nercfueltypegeneration_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in NercFuelTypeGeneration dataframe')

            # NercNonBaseloadValues
            try:
                nercnonbaseloadvalues_df = df[['nerc', 'nrnbnox', 'nrnbnxo',
                                                'nrnbso2', 'nrnbco2', 'nrnbch4', 'nrnbn2o',   
                                                'nrnbc2e', 'nrnbhg', 'nrnbgncl', 'nrnbgnol', 'nrnbgngs',  
                                                'nrnbgnnc', 'nrnbgnhy', 'nrnbgnbm', 'nrnbgnwi',  
                                                'nrnbgnso', 'nrnbgngt', 'nrnbgnof', 'nrnbgnop',  
                                                'nrnbclpr', 'nrnbolpr', 'nrnbgspr', 'nrnbncpr',  
                                                'nrnbhypr', 'nrnbbmpr', 'nrnbwipr', 'nrnbsopr',  
                                                'nrnbgtpr', 'nrnbofpr', 'nrnboppr']].copy()
                nercnonbaseloadvalues_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in NercNonBaseloadValues dataframe')

            # NercResourceMix
            try: 
                nercresourcemix_df = df[['nerc', 'nrclpr', 'nrolpr', 'nrgspr', 
                                        'nrncpr', 'nrhypr', 'nrbmpr', 'nrwipr', 
                                        'nrsopr', 'nrgtpr', 'nrofpr', 'nroppr', 
                                        'nrtnpr', 'nrtrpr', 'nrtopr', 'nrthpr', 
                                        'nrcypr', 'nrcnpr', 'nrcopr']].copy()
                nercresourcemix_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in NercResourceMix dataframe')

            try:
                # build temp tables, replace will replace the table if it already exists
                nerc_df.to_sql('nerc_temp', con=engine, if_exists='replace', index=False) 
                nercadjustedvalues_df.to_sql('nerc_adjusted_values_temp', con=engine, if_exists='replace', index=False)
                nercemissionrate_df.to_sql('nerc_emission_rate_temp', con=engine, if_exists='replace', index=False)
                nercfueltypeemissionrate_df.to_sql('nerc_fuel_type_emission_rate_temp', con=engine, if_exists='replace', index=False)
                nercfueltypegeneration_df.to_sql('nerc_fuel_type_generation_temp', con=engine, if_exists='replace', index=False)
                nercnonbaseloadvalues_df.to_sql('nerc_nonbaseload_values_temp', con=engine, if_exists='replace', index=False)
                nercresourcemix_df.to_sql('nerc_resource_mix_temp', con=engine, if_exists='replace', index=False)

                with engine.connect() as conn:
                    trans = conn.begin()
                    nerc_cnt = conn.execute(text("select count(*) from nerc;")).scalar()
                    
                    # count to see if table is empty
                    nercadjustedvalues_cnt = conn.execute(
                        text("select count(*) from nerc_adjusted_values where year = :year"),
                        {"year": int(year)}
                    ).scalar()  

                    nercemissionrate_cnt = conn.execute(
                        text("select count(*) from nerc_emission_rate where year = :year"),
                        {"year": int(year)}
                    ).scalar()

                    nercfueltypeemissionrate_cnt = conn.execute(
                        text("select count(*) from nerc_fuel_type_emission_rate where year = :year"),
                        {"year": int(year)}
                    ).scalar()

                    nercfueltypegeneration_cnt = conn.execute(
                        text("select count(*) from nerc_fuel_type_generation where year = :year"),
                        {"year": int(year)}
                    ).scalar()

                    nercnonbaseloadvalues_cnt = conn.execute(
                        text("select count(*) from nerc_nonbaseload_values where year = :year"),
                        {"year": int(year)}
                    ).scalar()

                    nercresourcemix_cnt = conn.execute(
                        text("select count(*) from nerc_resource_mix where year = :year"),
                        {"year": int(year)}
                    ).scalar()

                    # check count to insert or update the table
                    if nerc_cnt == 0:
                        conn.execute(text("""
                            insert into nerc (
                                nerc, nrname, nrnamepcap
                            ) select nerc, nrname, nrnamepcap 
                            from balancing_authority_temp;
                        """))  
                    else:
                        conn.execute(text("""
                            update balancing_authority 
                            set nerc = nrt.nerc, 
                                nrname = nrt.nrname,
                                nrnamepcap = nrt.nrnamepcap              
                            from nerc_temp nrt
                            where nerc.nerc = nrt.nerc;
                        """)) 

                    if nercadjustedvalues_cnt == 0:
                        sql = build_insert_from_temp_sql("nerc_adjusted_values", nercadjustedvalues_df)
                        conn.execute(text(sql))  
                    else:
                        sql = update_from_temp_table( "nerc_adjusted_values", nercadjustedvalues_df, "nerc")
                        conn.execute(text(sql))    

                    if nercemissionrate_cnt == 0:
                        sql = build_insert_from_temp_sql("nerc_emission_rate", nercemissionrate_df)
                        conn.execute(text(sql))  
                    else:
                        sql = update_from_temp_table("nerc_emission_rate", nercemissionrate_df, "nerc")
                        conn.execute(text(sql))  

                    if nercfueltypeemissionrate_cnt == 0:
                        sql = build_insert_from_temp_sql("nerc_fuel_type_emission_rate", nercfueltypeemissionrate_df)
                        conn.execute(text(sql))  
                    else:
                        sql = update_from_temp_table("nerc_fuel_type_emission_rate", nercfueltypeemissionrate_df, "nerc")
                        conn.execute(text(sql)) 

                    if nercfueltypegeneration_cnt == 0:
                        sql = build_insert_from_temp_sql("nerc_fuel_type_generation", nercfueltypegeneration_df)
                        conn.execute(text(sql))  
                    else:
                        sql = update_from_temp_table("nerc_fuel_type_generation", nercfueltypegeneration_df, "nerc")
                        conn.execute(text(sql)) 

                    if nercnonbaseloadvalues_cnt == 0:
                        sql = build_insert_from_temp_sql("nerc_nonbaseload_values", nercnonbaseloadvalues_df)
                        conn.execute(text(sql))  
                    else:
                        sql = update_from_temp_table("nerc_nonbaseload_values", nercnonbaseloadvalues_df, "nerc")
                        conn.execute(text(sql)) 

                    if nercresourcemix_cnt == 0:
                        sql = build_insert_from_temp_sql("nerc_resource_mix", nercresourcemix_df)
                        conn.execute(text(sql))  
                    else:
                        sql = update_from_temp_table("nerc_resource_mix", nercresourcemix_df, "nerc")
                        conn.execute(text(sql)) 

                    # drop temp tables
                    conn.execute(text("drop table nerc_temp;"))
                    conn.execute(text("drop table nerc_adjusted_values_temp;")) 
                    conn.execute(text("drop table nerc_emission_rate_temp;"))
                    conn.execute(text("drop table nerc_fuel_type_emission_rate_temp"))
                    conn.execute(text("drop table nerc_fuel_type_generation_temp"))
                    conn.execute(text("drop table nerc_nonbaseload_values_temp"))
                    conn.execute(text("drop table nerc_resource_mix_temp"))
                    trans.commit() 

                print('Success populating nerc data.')  
                  
            except Exception as e:
                print('Error populating nerc data.', e)
                return {"error": str(e)}  

            return {"success": True, "message": "Data successfully inserted into the NERC table."}
        else:
            return {"error": f"Failed to connect to R API with status code {response.status_code}"}
    
    except Exception as e:
        return {"error": str(e)}