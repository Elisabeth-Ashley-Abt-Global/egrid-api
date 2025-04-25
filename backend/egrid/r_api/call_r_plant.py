# File to communicate with the R API
import requests  
import logging
import pandas as pd  
from sqlalchemy import text 
from .utils import record_insert_update 
  
logger = logging.getLogger('egrid')
 
def populate_plant_data(engine=None, api_url=None, year=None):  
    print("Starting script to populate plant data for year ", year)
 
    try:
        response = requests.get(f"{api_url}{year}/plant")
        data = response.json()   
       
        if response.status_code == 200 and data.get('success'):
            plant_data = data.get('data', [])
            df = pd.DataFrame(plant_data)  

            cast_to_int = ['year', 'orispl', 'utlsrvid', 'numunt', 'numgen', 'oprcode', 'seqplt']

            # Define the new columns to type cast (2023+ data)
            new_cols = ['plngennb', 'plgenato', 'plgenaco', 'pltopr', 'plcopr', 'unco2e', 'bioco2e', 'chpco2e']
            # Define new columns for dataframes (2023+ data)
            new_resource_cols = ['pltopr','plcopr'] # PlantResourceMix
            new_ftg_cols = ['plgenato','plgenaco'] # PlantFuelTypeGeneration
            new_unadjusted_cols = ['unco2e', 'bioco2e', 'chpco2e', 'unc2esrc'] # PlantUnadjustedValues

            cast_to_float = ['lat', 'lon', 'plhtian', 'plhtioz',
                            'plhtiant', 'plhtiozt', 'plngenan', 'plngenoz', 
                            'plngennb', 'plnoxan', 'plnoxoz', 'plso2an',
                            'plco2an', 'plch4an', 'pln2oan', 'plco2eqa', 
                            'plnoxrta', 'plnoxrto', 'plso2rta', 'plco2rta',
                            'plch4rta', 'pln2orta', 'plc2erta', 'plnoxra',
                            'plnoxro', 'plso2ra', 'plco2ra', 'plch4ra',
                            'pln2ora', 'plc2era', 'plnoxcrt', 'plnoxcro',
                            'plso2crt', 'plco2crt', 'plch4crt', 'pln2ocrt',
                            'plc2ecrt', 'plgenacl', 'plgenaol', 'plgenags',
                            'plgenanc', 'plgenahy', 'plgenabm', 'plgenawi',
                            'plgenaso', 'plgenagt', 'plgenaof', 'plgenaop',
                            'plgenacy', 'plgenacn', 'plgenaco', 'plgenatn', 
                            'plgenatr', 'plgenato', 'plgenath', 'plclpr',
                            'plolpr', 'plgspr', 'plncpr', 'plhypr', 'plbmpr',
                            'plwipr', 'plsopr', 'plgtpr', 'plofpr', 'ploppr',
                            'pltnpr', 'pltrpr', 'pltopr', 'plthpr', 'plcypr',
                            'plcnpr', 'plcopr', 'unnox', 'unnoxoz', 'unso2',
                            'unco2', 'unch4', 'unn2o', 'unco2e', 'unhti',
                            'unhtioz', 'unhtit', 'unhtiozt', 'bionox', 'bionoxoz',
                            'bioso2', 'bioco2', 'bioch4', 'bion2o', 'bioco2e',
                            'chpchti', 'chpchtioz', 'chpnox', 'chpnoxoz', 'chpso2',
                            'chpco2', 'chpch4', 'chpn2o', 'chpco2e']
            
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
         
            # Plant
            plant_df = df[['fipsst', 'orispl', 'utlsrvid', 'bacode', 'subrgn',
                            'nerc', 'lat', 'lon', 'numunt', 'numgen', 'plprmfl', 
                            'plfuelct', 'oprcode', 'sector', 'pname', 'coalflag', 
                            'isorto']].copy()
            plant_df.replace({"--": pd.NA, "N/A": pd.NA, "": pd.NA}, inplace=True) # replace placeholders else you'll encounter  invalid input syntax for type double precision
            
            # PlantAdjustedValues
            #'plhgan'
            #'namepcap'
            try: 
                plantadjustedvalues_df = df[['year', 'orispl', 'plhtian', 'plhtioz',
                                            'plhtiant', 'plhtiozt', 'plngenan', 'plngenoz', 
                                            'plnoxan', 'plnoxoz', 'plso2an',
                                            'plco2an', 'plch4an', 'pln2oan', 'plco2eqa']].copy()
                if year >= 2023: 
                    plantadjustedvalues_df['plngennb'] = df['plngennb']

                plantadjustedvalues_df.copy()
                plantadjustedvalues_df.replace({"--": pd.NA, "N/A": pd.NA, "": pd.NA}, inplace=True) 
            except Exception: 
                print('Error in PlantAdjustedValues dataframe')

            # PlantEmissionRate
            #'plhgcrt'
            #plhgrta
            #plhgra
            try: 
                plantemissionrate_df = df[['year', 'orispl', 'plnoxrta', 'plnoxrto', 'plso2rta', 'plco2rta',
                                        'plch4rta', 'pln2orta', 'plc2erta', 'plnoxra',
                                        'plnoxro', 'plso2ra', 'plco2ra', 'plch4ra',
                                        'pln2ora', 'plc2era',  'plnoxcrt', 'plnoxcro',
                                        'plso2crt', 'plco2crt', 'plch4crt', 'pln2ocrt',
                                        'plc2ecrt']].copy()
                plantemissionrate_df.replace({"--": pd.NA, "N/A": pd.NA, "": pd.NA}, inplace=True) 
            except Exception: 
                print('Error in PlantEmissionRate dataframe')

            # PlantFuelTypeGeneration
            try: 
                plantfueltypegeneration_df = df[['year', 'orispl', 'plgenacl', 'plgenaol', 'plgenags',
                                                'plgenanc', 'plgenahy', 'plgenabm', 'plgenawi',
                                                'plgenaso', 'plgenagt', 'plgenaof', 'plgenaop',
                                                'plgenacy', 'plgenacn', 'plgenatn', 
                                                'plgenatr', 'plgenath']].copy()
                if year >= 2023: 
                    for col in new_ftg_cols: 
                        plantfueltypegeneration_df[col] = df[col]

                plantfueltypegeneration_df.copy()
                plantfueltypegeneration_df.replace({"--": pd.NA, "N/A": pd.NA, "": pd.NA}, inplace=True)
            except Exception: 
                print('Error in PlantFuelTypeGeneration dataframe')
            
            # PlantResourceMix
            try: 
                plantresourcemix_df = df[['year', 'orispl', 'plclpr',
                                        'plolpr', 'plgspr', 'plncpr', 'plhypr', 'plbmpr',
                                        'plwipr', 'plsopr', 'plgtpr', 'plofpr', 'ploppr',
                                        'pltnpr', 'pltrpr', 'plthpr', 'plcypr', 'plcnpr']].copy()
                if year >= 2023: 
                    for col in new_resource_cols: 
                        plantresourcemix_df[col] = df[col]

                plantresourcemix_df.copy()
                plantresourcemix_df.replace({"--": pd.NA, "N/A": pd.NA, "": pd.NA}, inplace=True)
            except Exception: 
                print('Error in PlantResourceMix dataframe')

            # PlantUnadjustedValues
            try: 
                plantunadjustedvalues_df = df[['year', 'orispl', 'unnox', 'unnoxoz', 'unso2',
                                            'unco2', 'unch4', 'unn2o', 'unhti',
                                            'unhtioz', 'unhtit', 'unhtiozt', 'unnoxsrc', 
                                            'unnozsrc', 'unso2src', 'unco2src', 'unch4src', 'unn2osrc', 
                                            'unhgsrc', 'unhtisrc', 'unhozsrc',
                                            'bionox', 'bionoxoz', 'bioso2', 'bioco2', 
                                            'bioch4', 'bion2o', 'chpchti', 
                                            'chpchtioz', 'chpnox', 'chpnoxoz', 'chpso2',
                                            'chpco2', 'chpch4', 'chpn2o']].copy()
                if year >= 2023: 
                    for col in new_unadjusted_cols: 
                        plantunadjustedvalues_df[col] = df[col]

                plantunadjustedvalues_df.copy()
                plantunadjustedvalues_df.replace({"--": pd.NA, "N/A": pd.NA, "": pd.NA}, inplace=True)
            except Exception: 
                print('Error PlantUnadjustedValues dataframe')

            tables = ["plant_adjusted_values", "plant_emission_rate",
                    "plant_fuel_type_generation", "plant_resource_mix", "plant_unadjusted_values"]
            
            df_map = {
                "plant_adjusted_values": plantadjustedvalues_df,
                "plant_emission_rate": plantemissionrate_df,
                "plant_fuel_type_generation": plantfueltypegeneration_df,
                "plant_resource_mix": plantresourcemix_df,
                "plant_unadjusted_values": plantunadjustedvalues_df
            }

            try:
                # build temp tables, replace will replace the table if it already exists
                plant_df.to_sql('plant_temp', con=engine, if_exists='replace', index=False)
                plantadjustedvalues_df.to_sql('plant_adjusted_values_temp', con=engine, if_exists='replace', index=False)
                plantemissionrate_df.to_sql('plant_emission_rate_temp', con=engine, if_exists='replace', index=False)
                plantfueltypegeneration_df.to_sql('plant_fuel_type_generation_temp', con=engine, if_exists='replace', index=False)
                plantresourcemix_df.to_sql('plant_resource_mix_temp', con=engine, if_exists='replace', index=False)
                plantunadjustedvalues_df.to_sql('plant_unadjusted_values_temp', con=engine, if_exists='replace', index=False)

                with engine.connect() as conn:
                    trans = conn.begin()
    
                    conn.execute(text("""
                        insert into plant (
                            orispl, fipsst, utlsrvid, bacode, subrgn, nerc, lat, lon,
                            numunt, numgen, plprmfl, plfuelct, oprcode, sector, pname,
                            coalflag, isorto
                        )
                        select
                            orispl, fipsst, utlsrvid, bacode, subrgn, nerc, lat, lon,
                            numunt, numgen, plprmfl, plfuelct, oprcode, sector, pname,
                            coalflag, isorto
                        from plant_temp
                        on conflict (orispl) do update
                        set
                            fipsst = excluded.fipsst,
                            utlsrvid = excluded.utlsrvid,
                            bacode = excluded.bacode,
                            subrgn = excluded.subrgn,
                            nerc = excluded.nerc,
                            lat = excluded.lat,
                            lon = excluded.lon,
                            numunt = excluded.numunt,
                            numgen = excluded.numgen,
                            plprmfl = excluded.plprmfl,
                            plfuelct = excluded.plfuelct,
                            oprcode = excluded.oprcode,
                            sector = excluded.sector,
                            pname = excluded.pname,
                            coalflag = excluded.coalflag, 
                            isorto = excluded.isorto;
                    """))

                    for table in tables:
                        try:
                            df = df_map[table]
                            if not df.empty:
                                sql = record_insert_update(table, df, unique_field="orispl")
                                conn.execute(text(sql))
                                print(f"Successfully upserted: {table}")
                            else:
                                print(f"Skipped empty DataFrame for: {table}")
                        except Exception as e:
                            print(f"Error processing {table}: {e}")

                    # drop temp tables
                    conn.execute(text("drop table plant_temp;"))
                    conn.execute(text("drop table plant_adjusted_values_temp;")) 
                    conn.execute(text("drop table plant_emission_rate_temp;"))
                    conn.execute(text("drop table plant_fuel_type_generation_temp"))
                    conn.execute(text("drop table plant_resource_mix_temp"))
                    conn.execute(text("drop table plant_unadjusted_values_temp;")) 
                    trans.commit() 
  
                print('Success populating plant data.')

            except Exception as e:
                print('Error populating plant data.', e)
                return {"error": str(e)}  

            return {"success": True, "message": "Data successfully inserted into the Plant table."}
        else:
            return {"error": f"Failed to connect to R API with status code {response.status_code}"}
    
    except Exception as e:
        return {"error": str(e)}

 