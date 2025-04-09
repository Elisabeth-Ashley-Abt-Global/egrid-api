# File to communicate with the R API
import requests  
import logging
import pandas as pd  
from sqlalchemy import text 
from .utils import update_from_temp_table, build_insert_from_temp_sql 


logger = logging.getLogger('egrid')
 
def populate_state_data(engine=None, api_url=None, year=None): 
    print('Populating State Data')
    logger.debug("*populate_state_data")

    try:
        response = requests.get(f"{api_url}{year}/state")
        data = response.json() 
        
        if response.status_code == 200 and data.get('success'):
            state_data = data.get('data', [])
            df = pd.DataFrame(state_data)
            # print(df.head())
            cast_to_int = ['year']
            
            # step 1
            # Define the new columns to type cast (2023+ data)
            new_cols = ['stngennb', 'stgenato','stgenaco','sttopr','stcopr']
            # Define new columns for dataframes (2023+ data)
            new_resource_cols = ['sttopr','stcopr']
            new_ftg_cols = ['stgenato','stgenaco']
               
            cast_to_float = ['stnamepcap', 'sthtian', 'sthtioz', 'sthtiant', 
                             'sthtiozt', 'stngenan', 'stngenoz', 'stngennb', 
                             'stnoxan', 'stnoxoz', 'stso2an', 'stco2an', 
                             'stch4an', 'stn2oan', 'stco2eqa', 'stnoxrta',
                             'stnoxrto', 'stso2rta', 'stco2rta', 'stch4rta', 
                             'stn2orta', 'stc2erta', 'stnoxra', 'stnoxro',
                             'stso2ra', 'stco2ra', 'stch4ra', 'stn2ora', 
                             'stc2era', 'stnoxcrt', 'stnoxcro', 'stso2crt', 
                             'stco2crt', 'stch4crt', 'stn2ocrt',  
                             'stcnoxrt', 'stonoxrt', 'stgnoxrt', 'stfsnxrt', 
                             'stcnxort', 'stonxort', 'stgnxort', 'stfsnort', 
                             'stcso2rt', 'stoso2rt', 'stgso2rt', 'stfss2rt', 
                             'stcco2rt', 'stoco2rt', 'stgco2rt', 'stfsc2rt', 
                             'stcch4rt', 'stoch4rt', 'stgch4rt', 'stfch4rt', 
                             'stcn2ort', 'ston2ort', 'stgn2ort', 'stfn2ort', 
                             'stcc2ert', 'stoc2ert', 'stgc2ert', 'stfsc2ert',
                             'stcnoxr', 'stonoxr', 'stgnoxr', 'stfsnxr',
                             'stcnxor', 'stonxor', 'stgnxor', 'stfsnor',
                             'stcso2r', 'stoso2r', 'stgso2r', 'stfss2r', 
                             'stcco2r', 'stoco2r', 'stgco2r', 'stfsc2r',
                             'stcch4r', 'stoch4r', 'stgch4r', 'stfch4r',
                             'stcn2or', 'ston2or', 'stgn2or', 'stfn2or', 
                             'stcc2er', 'stoc2er', 'stgc2er',  'stfsc2er', 
                             'stgenacl', 'stgenaol', 'stgenaso', 'stgenagt',
                             'stgenaof', 'stgenaop', 'stgenatn', 'stgenatr', 
                             'stgenato', 'stgenath', 'stgenacy', 'stgenacn',
                             'stgenaco', 'stgenags', 'stgenanc', 'stgenahy',
                             'stgenabm', 'stgenawi', 'stnbnox', 'stnbnxo',
                             'stnbso2', 'stnbco2', 'stnbch4', 'stnbn2o',   
                             'stnbc2e', 'stnbgncl', 'stnbgnol', 'stnbgngs',  
                             'stnbgnnc', 'stnbgnhy', 'stnbgnbm', 'stnbgnwi',  
                             'stnbgnso', 'stnbgngt', 'stnbgnof', 'stnbgnop',  
                             'stnbclpr', 'stnbolpr', 'stnbgspr', 'stnbncpr',  
                             'stnbhypr', 'stnbbmpr', 'stnbwipr', 'stnbsopr',  
                             'stnbgtpr', 'stnbofpr', 'stnboppr', 'stclpr',
                             'stolpr', 'stgspr', 'stncpr', 'sthypr', 
                             'stbmpr', 'stwipr', 'stsopr', 'stgtpr', 
                             'stofpr', 'stoppr', 'sttnpr', 'sttrpr',
                             'sttopr', 'stthpr', 'stcypr', 'stcnpr', 
                             'stcopr'] 
            #'stc2ecrt', 
          
            # step 2
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
            # State
            try:
                state_df = df[['fipsst', 'pstatabb', 'stnamepcap']].copy() 
            except Exception:
                print('Error in State dataframe')

            # StateAdjustedValues
            try: 
                stateadjustedvalues_df = df[['fipsst', 'sthtian', 'sthtioz', 'sthtiant', 
                                            'sthtiozt', 'stngenan', 'stngenoz',
                                            'stnoxan', 'stnoxoz', 'stso2an', 'stco2an', 
                                            'stch4an', 'stn2oan', 'stco2eqa', 'sthgan', 'year']].copy()
                if year >= 2023:
                    # add 'stngennb' column to stadjustedvalues_df for records from 2023 onward
                    stateadjustedvalues_df['stngennb'] = df['stngennb']
                 
                stateadjustedvalues_df.copy()
                stateadjustedvalues_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in StateAdjustedValues dataframe')

            # StateEmissionRate
            try: 
                stateemissionrate_df = df[['fipsst', 'stnoxrta', 'stnoxrto', 'stso2rta', 
                                        'stco2rta', 'stch4rta', 'stn2orta', 'stc2erta', 
                                        'sthgrta', 'stnoxra', 'stnoxro', 'stso2ra',  
                                        'stco2ra', 'stch4ra', 'stn2ora', 'stc2era',  
                                        'sthgra', 'stnoxcrt', 'stnoxcro', 'stso2crt', 
                                        'stco2crt', 'stch4crt', 'stn2ocrt',  
                                        'sthgcrt', 'year']].copy()
                
                #stc2ecrt
                stateemissionrate_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in StateEmissionRate dataframe')

            # StateFuelTypeEmissionRate
            try: 
                statefueltypeemissionrate_df = df[['fipsst', 'stcnoxrt', 'stonoxrt', 'stgnoxrt', 'stfsnxrt', 
                                                'stcnxort', 'stonxort', 'stgnxort', 'stfsnort', 
                                                'stcso2rt', 'stoso2rt', 'stgso2rt', 'stfss2rt', 
                                                'stcco2rt', 'stoco2rt', 'stgco2rt', 'stfsc2rt', 
                                                'stcch4rt', 'stoch4rt', 'stgch4rt', 'stfch4rt', 
                                                'stcn2ort', 'ston2ort', 'stgn2ort', 'stfn2ort', 
                                                'stcc2ert', 'stoc2ert', 'stgc2ert', 'stfsc2ert',
                                                'stchgrt', 'stfshgrt', 'stcnoxr', 'stonoxr', 
                                                'stgnoxr', 'stfsnxr', 'stcnxor', 'stonxor', 
                                                'stgnxor', 'stfsnor', 'stcso2r', 'stoso2r', 
                                                'stgso2r', 'stfss2r', 'stcco2r', 'stoco2r', 
                                                'stgco2r', 'stfsc2r', 'stcch4r', 'stoch4r', 
                                                'stgch4r', 'stfch4r', 'stcn2or', 'ston2or', 
                                                'stgn2or', 'stfn2or', 'stcc2er', 'stoc2er', 
                                                'stgc2er',  'stfsc2er', 'stchgr', 'stfshgr', 'year']].copy()
                statefueltypeemissionrate_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in StateFuelTypeEmissionRate dataframe')

            # StateFuelTypeGeneration
            try: 
                statefueltypegeneration_df = df[['fipsst', 'stgenacl', 'stgenaol', 'stgenaso', 'stgenagt',
                                                'stgenaof', 'stgenaop', 'stgenatn', 'stgenatr', 
                                                'stgenath', 'stgenacy', 'stgenacn',
                                                'stgenags', 'stgenanc', 'stgenahy',
                                                'stgenabm', 'stgenawi', 'year']].copy()
             
                if year >= 2023: 
                    for col in new_ftg_cols: 
                        statefueltypegeneration_df[col] = df[col]

                statefueltypegeneration_df.copy()
                statefueltypegeneration_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in StateFuelTypeGeneration dataframe')

            # StateNonBaseloadValues
            try:
                statenonbaseloadvalues_df = df[['fipsst', 'stnbnox', 'stnbnxo',
                                                'stnbso2', 'stnbco2', 'stnbch4', 'stnbn2o',   
                                                'stnbc2e', 'stnbhg', 'stnbgncl', 'stnbgnol', 'stnbgngs',  
                                                'stnbgnnc', 'stnbgnhy', 'stnbgnbm', 'stnbgnwi',  
                                                'stnbgnso', 'stnbgngt', 'stnbgnof', 'stnbgnop',  
                                                'stnbclpr', 'stnbolpr', 'stnbgspr', 'stnbncpr',  
                                                'stnbhypr', 'stnbbmpr', 'stnbwipr', 'stnbsopr',  
                                                'stnbgtpr', 'stnbofpr', 'stnboppr']].copy()
                statenonbaseloadvalues_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in StateNonBaseloadValues dataframe')

            # StateResourceMix
            try: 
                stateresourcemix_df = df[['fipsst', 'stclpr', 'stolpr', 'stgspr', 
                                        'stncpr', 'sthypr', 'stbmpr', 'stwipr', 
                                        'stsopr', 'stgtpr', 'stofpr', 'stoppr', 
                                        'sttnpr', 'sttrpr', 'stthpr', 
                                        'stcypr', 'stcnpr']].copy()

                if year >= 2023: 
                    for col in new_resource_cols: 
                        stateresourcemix_df[col] = df[col] 

                stateresourcemix_df.copy()
                stateresourcemix_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in StateResourceMix dataframe') 


            try:
                # build temp tables, replace will replace the table if it already exists
                state_df.to_sql('state_temp', con=engine, if_exists='replace', index=False) 
                stateadjustedvalues_df.to_sql('state_adjusted_values_temp', con=engine, if_exists='replace', index=False)
                stateemissionrate_df.to_sql('state_emission_rate_temp', con=engine, if_exists='replace', index=False)
                statefueltypeemissionrate_df.to_sql('state_fuel_type_emission_rate_temp', con=engine, if_exists='replace', index=False)
                statefueltypegeneration_df.to_sql('state_fuel_type_generation_temp', con=engine, if_exists='replace', index=False)
                statenonbaseloadvalues_df.to_sql('state_nonbaseload_values_temp', con=engine, if_exists='replace', index=False)
                stateresourcemix_df.to_sql('state_resource_mix_temp', con=engine, if_exists='replace', index=False)

                with engine.connect() as conn:
                    trans = conn.begin()
                    
                    # count to see if table is empty
                    state_cnt = conn.execute(text("select count(*) from state;")).scalar()

                    stateadjustedvalues_cnt = conn.execute(
                        text("select count(*) from state_adjusted_values where year = :year"),
                        {"year": int(year)}
                    ).scalar()  

                    stateemissionrate_cnt = conn.execute(
                        text("select count(*) from state_emission_rate where year = :year"),
                        {"year": int(year)}
                    ).scalar()

                    statefueltypeemissionrate_cnt = conn.execute(
                        text("select count(*) from state_fuel_type_emission_rate where year = :year"),
                        {"year": int(year)}
                    ).scalar()

                    statefueltypegeneration_cnt = conn.execute(
                        text("select count(*) from state_fuel_type_generation where year = :year"),
                        {"year": int(year)}
                    ).scalar()

                    statenonbaseloadvalues_cnt = conn.execute(
                        text("select count(*) from state_nonbaseload_values where year = :year"),
                        {"year": int(year)}
                    ).scalar()

                    stateresourcemix_cnt = conn.execute(
                        text("select count(*) from state_resource_mix where year = :year"),
                        {"year": int(year)}
                    ).scalar()

                    # check count to insert or update the table
                    if state_cnt == 0:
                        conn.execute(text("""
                            insert into state (
                                fipsst, pstatabb, stnamepcap
                            ) select fipsst, pstatabb, stnamepcap
                            from state_temp;
                        """))  
                    else:
                        conn.execute(text("""
                            update state
                            set fipsst = stt.fipsst, 
                                pstatabb = stt.pstatabb,
                                stnamepcap = stt.stnamepcap              
                            from state_temp stt
                            where state.fipsst = stt.fipsst;
                        """)) 

                    if stateadjustedvalues_cnt == 0:
                        sql = build_insert_from_temp_sql("state_adjusted_values", stateadjustedvalues_df)
                        conn.execute(text(sql))   
                    else:
                        sql = update_from_temp_table( "state_adjusted_values", stateadjustedvalues_df, "fipsst")
                        conn.execute(text(sql))     
 
                    if stateemissionrate_cnt == 0:
                        sql = build_insert_from_temp_sql("state_emission_rate", stateemissionrate_df)
                        conn.execute(text(sql))  
                    else:
                        sql = update_from_temp_table("state_emission_rate", stateemissionrate_df, "fipsst")
                        conn.execute(text(sql))  

                    if statefueltypeemissionrate_cnt == 0:
                        sql = build_insert_from_temp_sql("state_fuel_type_emission_rate", statefueltypeemissionrate_df)
                        conn.execute(text(sql))  
                    else:
                        sql = update_from_temp_table("state_fuel_type_emission_rate", statefueltypeemissionrate_df, "fipsst")
                        conn.execute(text(sql)) 

                    if statefueltypegeneration_cnt == 0:
                        sql = build_insert_from_temp_sql("state_fuel_type_generation", statefueltypegeneration_df)
                        conn.execute(text(sql))  
                    else:
                        sql = update_from_temp_table("state_fuel_type_generation", statefueltypegeneration_df, "fipsst")
                        conn.execute(text(sql)) 

                    if statenonbaseloadvalues_cnt == 0:
                        sql = build_insert_from_temp_sql("state_nonbaseload_values", statenonbaseloadvalues_df)
                        conn.execute(text(sql))  
                    else:
                        sql = update_from_temp_table("state_nonbaseload_values", statenonbaseloadvalues_df, "fipsst")
                        conn.execute(text(sql)) 

                    if stateresourcemix_cnt == 0:
                        sql = build_insert_from_temp_sql("state_resource_mix", stateresourcemix_df)
                        conn.execute(text(sql))  
                    else:
                        sql = update_from_temp_table("state_resource_mix", stateresourcemix_df, "fipsst")
                        conn.execute(text(sql)) 

                    # drop temp tables
                    conn.execute(text("drop table state_temp;"))
                    conn.execute(text("drop table state_adjusted_values_temp;")) 
                    conn.execute(text("drop table state_emission_rate_temp;"))
                    conn.execute(text("drop table state_fuel_type_emission_rate_temp"))
                    conn.execute(text("drop table state_fuel_type_generation_temp"))
                    conn.execute(text("drop table state_nonbaseload_values_temp"))
                    conn.execute(text("drop table state_resource_mix_temp"))
                    trans.commit() 

                print('Success populating state data.')  
                  
            except Exception as e:
                print('Error populating state data.', e)
                return {"error": str(e)}  

            return {"success": True, "message": "Data successfully inserted into the State table."}
        else:
            return {"error": f"Failed to connect to R API with status code {response.status_code}"}
    
    except Exception as e:
        return {"error": str(e)}