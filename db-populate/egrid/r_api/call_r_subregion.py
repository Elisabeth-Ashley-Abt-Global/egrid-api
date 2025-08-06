# File to communicate with the R API
import requests  
import logging
import pandas as pd  
from sqlalchemy import text 
from .utils import record_insert_update
 
logger = logging.getLogger('egrid')
 
def populate_subregion_data(engine=None, api_url=None, year=None): 
  
    print('Populating subregion data...') 

    try:
        response = requests.get(f"{api_url}{year}/subregion")
        data = response.json() 
      
        if response.status_code == 200 and data.get('success'):
          
            subregion_data = data.get('data', [])
            df = pd.DataFrame(subregion_data)
            #print('Subregion data:', df.head())
            cast_to_int = ['year']

            # Define the new columns to type cast (2023+ data)
            new_cols = ['srngennb','srgenato','srgenaco','srtopr','srcopr']
            # Define new columns for dataframes (2023+ data)
            new_resource_cols = ['srtopr','srcopr']
            new_ftg_cols = ['srgenato','srgenaco']

            cast_to_float = ['srnamepcap', 'srhtian', 'srhtioz', 'srhtiant', 
                             'srhtiozt', 'srngenan', 'srngenoz', 'srngennb', 
                             'srnoxan', 'srnoxoz', 'srso2an', 'srco2an', 
                             'srch4an', 'srn2oan', 'srco2eqa', 'srnoxrta',
                             'srnoxrto', 'srso2rta', 'srco2rta', 'srch4rta', 
                             'srn2orta', 'src2erta', 'srnoxra', 'srnoxro',
                             'srso2ra', 'srco2ra', 'srch4ra', 'srn2ora', 
                             'src2era', 'srnoxcrt', 'srnoxcro', 'srso2crt', 
                             'srco2crt', 'srch4crt', 'srn2ocrt', 'src2ecrt', 
                             'srcnoxrt', 'sronoxrt', 'srgnoxrt', 'srfsnxrt', 
                             'srcnxort', 'sronxort', 'srgnxort', 'srfsnort', 
                             'srcso2rt', 'sroso2rt', 'srgso2rt', 'srfss2rt', 
                             'srcco2rt', 'sroco2rt', 'srgco2rt', 'srfsc2rt', 
                             'srcch4rt', 'sroch4rt', 'srgch4rt', 'srfch4rt', 
                             'srcn2ort', 'sron2ort', 'srgn2ort', 'srfn2ort', 
                             'srcc2ert', 'sroc2ert', 'srgc2ert', 'srfsc2ert',
                             'srcnoxr', 'sronoxr', 'srgnoxr', 'srfsnxr',
                             'srcnxor', 'sronxor', 'srgnxor', 'srfsnor',
                             'srcso2r', 'sroso2r', 'srgso2r', 'srfss2r', 
                             'srcco2r', 'sroco2r', 'srgco2r', 'srfsc2r',
                             'srcch4r', 'sroch4r', 'srgch4r', 'srfch4r',
                             'srcn2or', 'sron2or', 'srgn2or', 'srfn2or', 
                             'srcc2er', 'sroc2er', 'srgc2er',  'srfsc2er', 
                             'srgenacl', 'srgenaol', 'srgenaso', 'srgenagt',
                             'srgenaof', 'srgenaop', 'srgenatn', 'srgenatr', 
                             'srgenato', 'srgenath', 'srgenacy', 'srgenacn',
                             'srgenaco', 'srgenags', 'srgenanc', 'srgenahy',
                             'srgenabm', 'srgenawi', 'srnbnox', 'srnbnxo',
                             'srnbso2', 'srnbco2', 'srnbch4', 'srnbn2o',   
                             'srnbc2e', 'srnbgncl', 'srnbgnol', 'srnbgngs',  
                             'srnbgnnc', 'srnbgnhy', 'srnbgnbm', 'srnbgnwi',  
                             'srnbgnso', 'srnbgngt', 'srnbgnof', 'srnbgnop',  
                             'srnbclpr', 'srnbolpr', 'srnbgspr', 'srnbncpr',  
                             'srnbhypr', 'srnbbmpr', 'srnbwipr', 'srnbsopr',  
                             'srnbgtpr', 'srnbofpr', 'srnboppr', 'srclpr',
                             'srolpr', 'srgspr', 'srncpr', 'srhypr', 
                             'srbmpr', 'srwipr', 'srsopr', 'srgtpr', 
                             'srofpr', 'sroppr', 'srtnpr', 'srtrpr',
                             'srtopr', 'srthpr', 'srcypr', 'srcnpr', 
                             'srcopr']
    
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
            # Subregion
            subregion_df = df[['subrgn', 'srname']].copy() 

            # SubrgnAdjustedValues
            try: 
                subrgnadjustedvalues_df = df[['subrgn', 'srnamepcap', 'srhtian', 'srhtioz', 'srhtiant', 
                                            'srhtiozt', 'srngenan', 'srngenoz',  
                                            'srnoxan', 'srnoxoz', 'srso2an', 'srco2an', 
                                            'srch4an', 'srn2oan', 'srco2eqa', 'srhgan', 'year']].copy()
                if year >= 2023: 
                    # add 'srngennb' column to subrgnadjustedvalues_df for records from 2023 onward
                    subrgnadjustedvalues_df['srngennb'] = df['srngennb']

                subrgnadjustedvalues_df.copy()
                subrgnadjustedvalues_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in SubrgnAdjustedValues dataframe')

            # SubrgnEmissionRate
            try: 
                subrgnemissionrate_df = df[['subrgn', 'srnoxrta', 'srnoxrto', 'srso2rta', 
                                        'srco2rta', 'srch4rta', 'srn2orta', 'src2erta', 
                                        'srhgrta', 'srnoxra', 'srnoxro', 'srso2ra',  
                                        'srco2ra', 'srch4ra', 'srn2ora', 'src2era',  
                                        'srhgra', 'srnoxcrt', 'srnoxcro', 'srso2crt', 
                                        'srco2crt', 'srch4crt', 'srn2ocrt', 'src2ecrt', 
                                        'srhgcrt', 'year']].copy()
                subrgnemissionrate_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in SubrgnEmissionRate dataframe')

            # SubrgnFuelTypeEmissionRate
            try: 
                subrgnfueltypeemissionrate_df = df[['subrgn', 'srcnoxrt', 'sronoxrt', 'srgnoxrt', 'srfsnxrt', 
                                                'srcnxort', 'sronxort', 'srgnxort', 'srfsnort', 
                                                'srcso2rt', 'sroso2rt', 'srgso2rt', 'srfss2rt', 
                                                'srcco2rt', 'sroco2rt', 'srgco2rt', 'srfsc2rt', 
                                                'srcch4rt', 'sroch4rt', 'srgch4rt', 'srfch4rt', 
                                                'srcn2ort', 'sron2ort', 'srgn2ort', 'srfn2ort', 
                                                'srcc2ert', 'sroc2ert', 'srgc2ert', 'srfsc2ert',
                                                'srchgrt', 'srfshgrt', 'srcnoxr', 'sronoxr', 
                                                'srgnoxr', 'srfsnxr', 'srcnxor', 'sronxor', 
                                                'srgnxor', 'srfsnor', 'srcso2r', 'sroso2r', 
                                                'srgso2r', 'srfss2r', 'srcco2r', 'sroco2r', 
                                                'srgco2r', 'srfsc2r', 'srcch4r', 'sroch4r', 
                                                'srgch4r', 'srfch4r', 'srcn2or', 'sron2or', 
                                                'srgn2or', 'srfn2or', 'srcc2er', 'sroc2er', 
                                                'srgc2er',  'srfsc2er', 'srchgr', 'srfshgr', 'year']].copy()
                subrgnfueltypeemissionrate_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in SubrgnFuelTypeEmissionRate dataframe')

            # SubrgnFuelTypeGeneration
            try: 
                subrgnfueltypegeneration_df = df[['subrgn', 'srgenacl', 'srgenaol', 'srgenaso', 'srgenagt',
                                                'srgenaof', 'srgenaop', 'srgenatn', 'srgenatr', 
                                                'srgenath', 'srgenacy', 'srgenacn',
                                                'srgenags', 'srgenanc', 'srgenahy',
                                                'srgenabm', 'srgenawi', 'year']].copy()
                if year >= 2023: 
                    for col in new_ftg_cols:
                        subrgnfueltypegeneration_df[col] = df[col]

                subrgnfueltypegeneration_df.copy()
                subrgnfueltypegeneration_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in SubrgnFuelTypeGeneration dataframe')

            # SubrgnNonBaseloadValues
            try:
                subrgnnonbaseloadvalues_df = df[['subrgn', 'srnbnox', 'srnbnxo',
                                                'srnbso2', 'srnbco2', 'srnbch4', 'srnbn2o',   
                                                'srnbc2e', 'srnbhg', 'srnbgncl', 'srnbgnol', 'srnbgngs',  
                                                'srnbgnnc', 'srnbgnhy', 'srnbgnbm', 'srnbgnwi',  
                                                'srnbgnso', 'srnbgngt', 'srnbgnof', 'srnbgnop',  
                                                'srnbclpr', 'srnbolpr', 'srnbgspr', 'srnbncpr',  
                                                'srnbhypr', 'srnbbmpr', 'srnbwipr', 'srnbsopr',  
                                                'srnbgtpr', 'srnbofpr', 'srnboppr']].copy()
                subrgnnonbaseloadvalues_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in SubrgnNonBaseloadValues dataframe')

            # SubrgnResourceMix
            try: 
                subrgnresourcemix_df = df[['subrgn', 'srclpr', 'srolpr', 'srgspr', 
                                        'srncpr', 'srhypr', 'srbmpr', 'srwipr', 
                                        'srsopr', 'srgtpr', 'srofpr', 'sroppr', 
                                        'srtnpr', 'srtrpr', 'srthpr', 
                                        'srcypr', 'srcnpr']].copy()
                if year >= 2023: 
                    for col in new_resource_cols: 
                        subrgnresourcemix_df[col] = df[col]

                subrgnresourcemix_df.copy()
                subrgnresourcemix_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in SubrgnResourceMix dataframe')

            tables = ["subrgn_adjusted_values", "subrgn_emission_rate", "subrgn_fuel_type_emission_rate", 
                      "subrgn_fuel_type_generation", "subrgn_nonbaseload_values", "subrgn_resource_mix"]

            df_map = {
                "subrgn_adjusted_values": subrgnadjustedvalues_df,
                "subrgn_emission_rate": subrgnemissionrate_df,
                "subrgn_fuel_type_emission_rate": subrgnfueltypeemissionrate_df,
                "subrgn_fuel_type_generation": subrgnfueltypegeneration_df,
                "subrgn_nonbaseload_values": subrgnnonbaseloadvalues_df,
                "subrgn_resource_mix": subrgnresourcemix_df
            }

            try:
                # build temp tables, replace will replace the table if it already exists
                subregion_df.to_sql('subregion_temp', con=engine, if_exists='replace', index=False) 
                subrgnadjustedvalues_df.to_sql('subrgn_adjusted_values_temp', con=engine, if_exists='replace', index=False)
                subrgnemissionrate_df.to_sql('subrgn_emission_rate_temp', con=engine, if_exists='replace', index=False)
                subrgnfueltypeemissionrate_df.to_sql('subrgn_fuel_type_emission_rate_temp', con=engine, if_exists='replace', index=False)
                subrgnfueltypegeneration_df.to_sql('subrgn_fuel_type_generation_temp', con=engine, if_exists='replace', index=False)
                subrgnnonbaseloadvalues_df.to_sql('subrgn_nonbaseload_values_temp', con=engine, if_exists='replace', index=False)
                subrgnresourcemix_df.to_sql('subrgn_resource_mix_temp', con=engine, if_exists='replace', index=False)
                
                with engine.connect() as conn:
                    trans = conn.begin()
                    
                    conn.execute(text("""insert into subregion (subrgn, srname)
                                        select subrgn, srname
                                        from subregion_temp
                                        on conflict (subrgn) do update 
                                        set srname = excluded.srname;"""))
                    
                    for table in tables:
                        try:
                            df = df_map[table]
                            if not df.empty:
                                sql = record_insert_update(table, df, unique_field="subrgn")
                                conn.execute(text(sql))
                                print(f"Successfully upserted: {table}")
                            else:
                                print(f"Skipped empty DataFrame for: {table}")
                        except Exception as e:
                            print(f"Error processing {table}: {e}")

                    # drop temp tables
                    conn.execute(text("drop table subregion_temp;"))
                    conn.execute(text("drop table subrgn_adjusted_values_temp;")) 
                    conn.execute(text("drop table subrgn_emission_rate_temp;"))
                    conn.execute(text("drop table subrgn_fuel_type_emission_rate_temp"))
                    conn.execute(text("drop table subrgn_fuel_type_generation_temp"))
                    conn.execute(text("drop table subrgn_nonbaseload_values_temp"))
                    conn.execute(text("drop table subrgn_resource_mix_temp"))
                    trans.commit() 

                print('Success populating subregion data.')  
                  
            except Exception as e:
                print('Error populating subregion data.', e)
                return {"error": str(e)}  

            return {"success": True, "message": "Data successfully inserted into the Subregion table."}
        else:
            return {"error": f"Failed to connect to R API with status code {response.status_code}"}
    
    except Exception as e:
        return {"error": str(e)}