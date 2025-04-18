# File to communicate with the R API
import requests  
import logging
import pandas as pd  
from sqlalchemy import text 
from .utils import record_insert_update

logger = logging.getLogger('egrid')
  
def populate_balancing_auth_data(engine=None, api_url=None, year=None):
    print("Starting script to populate balancing authority data for year ", year)
 
    try:
        response = requests.get(f"{api_url}{year}/balancingauthority")
        data = response.json()  
        
        if response.status_code == 200 and data.get('success'):
            ba_data = data.get('data', [])
            df = pd.DataFrame(ba_data) 

            cast_to_int = ['year']

            # Define the new columns to type cast (2023+ data)
            new_cols = ['bangennb','bagenato','bagenaco','batopr','bacopr']
            # Define new columns for dataframes (2023+ data)
            new_resource_cols = ['batopr','bacopr']
            new_ftg_cols = ['bagenato','bagenaco']

            cast_to_float = ['banamepcap', 'bahtian', 'bahtioz', 'bahtiant', 
                            'bahtiozt', 'bangenan', 'bangenoz', 'bangennb', 'banoxan', 'banoxoz', 
                            'baso2an', 'baco2an', 'bach4an', 'ban2oan', 'baco2eqa', 
                            'banoxrta', 'banoxrto', 'baso2rta', 'baco2rta', 'bach4rta', 'ban2orta', 'bac2erta',
                            'banoxra', 'banoxro', 'baso2ra', 'baco2ra', 'bach4ra', 'ban2ora', 'bac2era',
                            'banoxcrt', 'banoxcro', 'baso2crt', 'baco2crt', 'bach4crt', 'ban2ocrt', 'bac2ecrt', 'bahgcrt',
                            'bacnoxrt', 'baonoxrt', 'bagnoxrt', 'bafsnxrt', 'bacnxort', 'baonxort', 'bagnxort', 'bafsnort', 'bacso2rt',
                            'baoso2rt', 'bagso2rt', 'bafss2rt', 'bacco2rt', 'baoco2rt', 'bagco2rt', 'bafsc2rt', 'bacch4rt', 'baoch4rt',
                            'bagch4rt', 'bafch4rt', 'bacn2ort', 'baon2ort', 'bagn2ort', 'bafn2ort', 'bacc2ert', 'baoc2ert', 'bagc2ert',
                            'bafsc2er', 'bacnoxr', 'baonoxr', 'bagnoxr', 'bafsnxr', 'bacnxor', 'baonxor', 'bagnxor', 'bafsnor',
                            'bacso2r', 'baoso2r', 'bagso2r', 'bafss2r', 'bacco2r', 'baoco2r', 'bagco2r', 'bafsc2r', 'bacch4r',
                            'baoch4r', 'bagch4r', 'bafch4r', 'bacn2or', 'baon2or', 'bagn2or', 'bafn2or', 'bacc2er', 'baoc2er',
                            'bagc2er', 'bafsc2er', 'bagenacl', 'bagenaol', 'bagenaso', 'bagenagt', 'bagenaof', 'bagenaop', 'bagenatn', 'bagenatr', 
                            'bagenato', 'bagenath', 'bagenacy', 'bagenacn', 'bagenaco', 'bagenags', 'bagenanc', 'bagenahy',
                            'bagenabm', 'bagenawi', 'banbnox', 'banbnxo', 'banbso2', 'banbco2', 'banbch4', 'banbn2o',   
                            'banbc2e', 'banbgncl', 'banbgnol', 'banbgngs', 'banbgnnc', 'banbgnhy', 'banbgnbm', 'banbgnwi',  
                            'banbgnso', 'banbgngt', 'banbgnof', 'banbgnop', 'banbclpr', 'banbolpr', 'banbgspr', 'banbncpr',  
                            'banbhypr', 'banbbmpr', 'banbwipr', 'banbsopr', 'banbgtpr', 'banbofpr', 'banboppr', 'baclpr',
                            'baolpr', 'bagspr', 'bancpr', 'bahypr', 'babmpr', 'bawipr', 'basopr', 'bagtpr', 
                            'baofpr', 'baoppr', 'batnpr', 'batrpr', 'batopr', 'bathpr', 'bacypr', 'bacnpr', 'bacopr','bahgan']
            
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
          
            # BalancingAuthority
            ba_df = df[['bacode', 'baname', 'banamepcap']] 

            # BaAdjustedValues
            try: 
                # include og columns in the dataframe
                baadjustedvalues_df = df[['bacode', 'year', 'bahtian', 'bahtioz', 
                                          'bahtiant', 'bahtiozt', 'bangenan', 'bangenoz',
                                          'banoxan', 'banoxoz', 'baso2an', 'baco2an', 
                                          'bach4an', 'ban2oan', 'baco2eqa', 'bahgan']]
                
              
                if year >= 2023:
                    # add 'bangennb' column to baadjustedvalues_df for records from 2023 onward
                    baadjustedvalues_df['bangennb'] = df['bangennb']

                baadjustedvalues_df.copy()
                baadjustedvalues_df.replace({"--": None, "N/A": None, "": None}, inplace=True) # replace placeholders else you'll encounter  invalid input syntax for type double precision
            except Exception: 
                print('Error in BaAdjustedValues dataframe')

            # BaEmissionRate
            try:  
                baemissionrate_df = df[['bacode', 'year', 'banoxrta','banoxrto',
                                        'baso2rta', 'baco2rta', 'bach4rta', 'ban2orta',
                                        'bac2erta', 'bahgrta', 'banoxra', 'banoxro',
                                        'baso2ra', 'baco2ra', 'bach4ra', 'ban2ora', 
                                        'bac2era', 'bahgra', 'banoxcrt', 'banoxcro', 
                                        'baso2crt', 'baco2crt', 'bach4crt', 'ban2ocrt', 
                                        'bahgcrt', 'bac2ecrt']].copy() # field:  'bac2ecrt' is failing
                baemissionrate_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception:
                print('Error in BaEmissionRate dataframe')

            # BaFuelTypeEmissionRate
            try: 
                bafueltypeemissionrate_df = df[['bacode', 'bacnoxrt', 'baonoxrt', 'bagnoxrt', 'bafsnxrt', 
                                                'bacnxort', 'baonxort', 'bagnxort', 'bafsnort', 
                                                'bacso2rt', 'baoso2rt', 'bagso2rt', 'bafss2rt', 
                                                'bacco2rt', 'baoco2rt', 'bagco2rt', 'bafsc2rt', 
                                                'bacch4rt', 'baoch4rt', 'bagch4rt', 'bafch4rt', 
                                                'bacn2ort', 'baon2ort', 'bagn2ort', 'bafn2ort', 
                                                'bacc2ert', 'baoc2ert', 'bagc2ert', 'bafsc2ert',
                                                'bachgrt', 'bafshgrt', 'bacnoxr', 'baonoxr', 
                                                'bagnoxr', 'bafsnxr', 'bacnxor', 'baonxor', 
                                                'bagnxor', 'bafsnor', 'bacso2r', 'baoso2r', 
                                                'bagso2r', 'bafss2r', 'bacco2r', 'baoco2r', 
                                                'bagco2r', 'bafsc2r', 'bacch4r', 'baoch4r', 
                                                'bagch4r', 'bafch4r', 'bacn2or', 'baon2or', 
                                                'bagn2or', 'bafn2or', 'bacc2er', 'baoc2er', 
                                                'bagc2er',  'bafsc2er', 'bachgr', 'bafshgr', 'year']].copy()
                bafueltypeemissionrate_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in BaFuelTypeEmissionRate dataframe')

            # BaFuelTypeGeneration
            try: 
                bafueltypegeneration_df = df[['bacode', 'bagenacl', 'bagenaol', 'bagenaso', 'bagenagt',
                                            'bagenaof', 'bagenaop', 'bagenatn', 'bagenatr', 
                                            'bagenath', 'bagenacy', 'bagenacn',
                                            'bagenags', 'bagenanc', 'bagenahy',
                                            'bagenabm', 'bagenawi', 'year']].copy()
                if year >= 2023: 
                    for col in new_ftg_cols: 
                        bafueltypegeneration_df[col] = df[col]
                
                bafueltypegeneration_df.copy()
                bafueltypegeneration_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in BaFuelTypeGeneration dataframe')

            # BaNonBaseloadValues
            try:
                banonbaseloadvalues_df = df[['bacode', 'banbnox', 'banbnxo',
                                            'banbso2', 'banbco2', 'banbch4', 'banbn2o',   
                                            'banbc2e', 'banbhg', 'banbgncl', 'banbgnol', 'banbgngs',  
                                            'banbgnnc', 'banbgnhy', 'banbgnbm', 'banbgnwi',  
                                            'banbgnso', 'banbgngt', 'banbgnof', 'banbgnop',  
                                            'banbclpr', 'banbolpr', 'banbgspr', 'banbncpr',  
                                            'banbhypr', 'banbbmpr', 'banbwipr', 'banbsopr',  
                                            'banbgtpr', 'banbofpr', 'banboppr', 'year']].copy()
                banonbaseloadvalues_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in BaNonBaseloadValues dataframe')

            # BaResourceMix
            try: 
                baresourcemix_df = df[['bacode', 'baclpr', 'baolpr', 'bagspr', 
                                        'bancpr', 'bahypr', 'babmpr', 'bawipr', 
                                        'basopr', 'bagtpr', 'baofpr', 'baoppr', 
                                        'batnpr', 'batrpr', 'bathpr', 
                                        'bacypr', 'bacnpr', 'year']].copy()
                if year >= 2023: 
                    for col in new_resource_cols: 
                        baresourcemix_df[col] = df[col]

                baresourcemix_df.copy()
                baresourcemix_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in BaResourceMix dataframe')
 
            tables = ["ba_adjusted_values", "ba_emission_rate", "ba_fuel_type_emission_rate", "ba_fuel_type_generation", "ba_nonbaseload_values", "ba_resource_mix"]

            df_map = {
                "ba_adjusted_values": baadjustedvalues_df,
                "ba_emission_rate": baemissionrate_df,
                "ba_fuel_type_emission_rate": bafueltypeemissionrate_df,
                "ba_fuel_type_generation": bafueltypegeneration_df,
                "ba_nonbaseload_values": banonbaseloadvalues_df,
                "ba_resource_mix": baresourcemix_df
            }
           
            try:
                # build temp tables, replace will replace the table if it already exists
                ba_df.to_sql('balancing_authority_temp', con=engine, if_exists='replace', index=False) 
                baadjustedvalues_df.to_sql('ba_adjusted_values_temp', con=engine, if_exists='replace', index=False)
                baemissionrate_df.to_sql('ba_emission_rate_temp', con=engine, if_exists='replace', index=False)
                bafueltypeemissionrate_df.to_sql('ba_fuel_type_emission_rate_temp', con=engine, if_exists='replace', index=False)
                bafueltypegeneration_df.to_sql('ba_fuel_type_generation_temp', con=engine, if_exists='replace', index=False)
                banonbaseloadvalues_df.to_sql('ba_nonbaseload_values_temp', con=engine, if_exists='replace', index=False)
                baresourcemix_df.to_sql('ba_resource_mix_temp', con=engine, if_exists='replace', index=False)

                with engine.connect() as conn:
                    trans = conn.begin()
 
                    conn.execute(text("""insert into balancing_authority (bacode, baname, banamepcap)
                                        select bacode, baname, banamepcap
                                        from balancing_authority_temp
                                        on conflict (bacode) do update 
                                        set baname = excluded.baname,
                                        banamepcap = excluded.banamepcap;"""))
                    
                    for table in tables:
                        try:
                            df = df_map[table]
                            if not df.empty:
                                sql = record_insert_update(table, df, unique_field="bacode")
                                conn.execute(text(sql))
                                print(f"Successfully upserted: {table}")
                            else:
                                print(f"Skipped empty DataFrame for: {table}")
                        except Exception as e:
                            print(f"Error processing {table}: {e}")
                   
                    # drop temp tables
                    conn.execute(text("drop table balancing_authority_temp;"))
                    conn.execute(text("drop table ba_adjusted_values_temp;")) 
                    conn.execute(text("drop table ba_emission_rate_temp;"))
                    conn.execute(text("drop table ba_fuel_type_emission_rate_temp"))
                    conn.execute(text("drop table ba_fuel_type_generation_temp"))
                    conn.execute(text("drop table ba_nonbaseload_values_temp"))
                    conn.execute(text("drop table ba_resource_mix_temp"))
                    trans.commit() 

                print('Success populating balancing authority data.')  
                  
            except Exception as e:
                print('Error populating balancing authority data.', e)
                return {"error": str(e)}  

            return {"success": True, "message": "Data successfully inserted into the Balancing Authority table."}
        else:
            return {"error": f"Failed to connect to R API with status code {response.status_code}"}
    
    except Exception as e:
        return {"error": str(e)}