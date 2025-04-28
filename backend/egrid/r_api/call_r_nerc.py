# File to communicate with the R API
import requests  
import logging
import pandas as pd  
from sqlalchemy import text 
from .utils import record_insert_update

logger = logging.getLogger('egrid')
 
def populate_nerc_data(engine=None, api_url=None, year=None): 
    print("Starting script to populate nerc data for year ", year)

    try:
        response = requests.get(f"{api_url}{year}/nerc")
        data = response.json() 
        
        if response.status_code == 200 and data.get('success'):
            nerc_data = data.get('data', [])
            df = pd.DataFrame(nerc_data)
            #print('nerc data', df.head()) # for debugging
            cast_to_int = ['year']

            # Define the new columns to type cast (2023+ data)
            new_cols = ['nrngennb','nrgenato','nrgenaco','nrtopr','nrcopr']
            # Define new columns for dataframes (2023+ data)
            new_resource_cols = ['nrtopr','nrcopr']
            new_ftg_cols = ['nrgenato','nrgenaco']

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
            # cast nerc to char
            df['nerc'] = df['nerc'].astype(str).str.strip()

            nerc_df = df[['nerc', 'nercname']].copy() 

            # NercAdjustedValues
            try: 
                nercadjustedvalues_df = df[['nerc', 'nrnamepcap', 'nrhtian', 'nrhtioz', 'nrhtiant', 
                                            'nrhtiozt', 'nrngenan', 'nrngenoz', 
                                            'nrnoxan', 'nrnoxoz', 'nrso2an', 'nrco2an', 
                                            'nrch4an', 'nrn2oan', 'nrco2eqa', 'nrhgan', 'year']].copy()
                if year >= 2023: 
                    nercadjustedvalues_df['nrngennb'] = df['nrngennb']

                nercadjustedvalues_df.copy()
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
                                                'nrgenath', 'nrgenacy', 'nrgenacn',
                                                'nrgenags', 'nrgenanc', 'nrgenahy',
                                                'nrgenabm', 'nrgenawi', 'year']].copy()
                if year >= 2023: 
                    for col in new_ftg_cols: 
                        nercfueltypegeneration_df[col] = df[col]
                
                nercfueltypegeneration_df.copy()
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
                                        'nrtnpr', 'nrtrpr', 'nrthpr',
                                        'nrcypr', 'nrcnpr']].copy()
                if year >= 2023: 
                    for col in new_resource_cols: 
                        nercresourcemix_df[col] = df[col]
                
                nercresourcemix_df.copy()
                nercresourcemix_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in NercResourceMix dataframe')

            tables = ["nerc_adjusted_values", "nerc_emission_rate", "nerc_fuel_type_emission_rate",
                    "nerc_fuel_type_generation", "nerc_nonbaseload_values", "nerc_resource_mix"]
            
            df_map = {
                "nerc_adjusted_values": nercadjustedvalues_df,
                "nerc_emission_rate": nercemissionrate_df,
                "nerc_fuel_type_emission_rate": nercfueltypeemissionrate_df, 
                "nerc_fuel_type_generation": nercfueltypegeneration_df,
                "nerc_nonbaseload_values": nercnonbaseloadvalues_df, 
                "nerc_resource_mix": nercresourcemix_df
            }

            try:
                # build temp tables, replace will replace the table if it already exists
                nerc_df.to_sql('nerc_region_temp', con=engine, if_exists='replace', index=False) 
                nercadjustedvalues_df.to_sql('nerc_adjusted_values_temp', con=engine, if_exists='replace', index=False)
                nercemissionrate_df.to_sql('nerc_emission_rate_temp', con=engine, if_exists='replace', index=False)
                nercfueltypeemissionrate_df.to_sql('nerc_fuel_type_emission_rate_temp', con=engine, if_exists='replace', index=False)
                nercfueltypegeneration_df.to_sql('nerc_fuel_type_generation_temp', con=engine, if_exists='replace', index=False)
                nercnonbaseloadvalues_df.to_sql('nerc_nonbaseload_values_temp', con=engine, if_exists='replace', index=False)
                nercresourcemix_df.to_sql('nerc_resource_mix_temp', con=engine, if_exists='replace', index=False)

                with engine.connect() as conn:
                    trans = conn.begin()
                    conn.execute(text("""insert into nerc_region (nerc, nercname)
                                        select nerc, nercname
                                        from nerc_region_temp
                                        on conflict (nerc) do update 
                                        set nercname = excluded.nercname;"""))
                    
                    for table in tables:
                        try:
                            df = df_map[table]
                            if not df.empty:
                                sql = record_insert_update(table, df, unique_field="nerc")
                                conn.execute(text(sql))
                                print(f"Successfully upserted: {table}")
                            else:
                                print(f"Skipped empty DataFrame for: {table}")
                        except Exception as e:
                            print(f"Error processing {table}: {e}")

                    # drop temp tables
                    conn.execute(text("drop table nerc_region_temp;"))
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