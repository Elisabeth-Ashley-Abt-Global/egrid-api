# File to communicate with the R API
import requests  
import logging
import pandas as pd  
from sqlalchemy import text 
from .utils import update_from_temp_table, build_insert_from_temp_sql 
  

logger = logging.getLogger('egrid')
 
def populate_plant_data(engine=None, api_url=None): 
    print('populate_plant_data')
    logger.debug("*populate_plant_data")

    try:
        response = requests.get(f"{api_url}plant")
        data = response.json() 
       
        if response.status_code == 200 and data.get('success'):
            plant_data = data.get('data', [])
            df = pd.DataFrame(plant_data) 

            cast_to_int = ['year', 'orispl', 'utlsrvid', 'numunt', 'numgen', 'oprcode', 'seqplt' ]
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
            
            for col in cast_to_int:
                df[col] = pd.to_numeric(df[col], errors='coerce').astype("Int64")

            for col in cast_to_float:
                df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)

            year = df['year'].unique()[0] 
            print('year ', year)

            # create tables
            # Plant
            plant_df = df[['pstatabb', 'fipsst', 'orispl', 'utlsrvid', 'bacode', 
                            'nerc', 'lat', 'lon', 'numunt', 'numgen', 'plprmfl', 
                            'plfuelct', 'oprcode', 'sector', 'pname', 'coalflag', 'seqplt']].copy()
            plant_df.replace({"--": pd.NA, "N/A": pd.NA, "": pd.NA}, inplace=True) # replace placeholders else you'll encounter  invalid input syntax for type double precision
            
            # PlantAdjustedValues
            try: 
                plantadjustedvalues_df = df[['year', 'orispl', 'plhtian', 'plhtioz',
                                            'plhtiant', 'plhtiozt', 'plngenan', 'plngenoz', 
                                            'plngennb', 'plnoxan', 'plnoxoz', 'plso2an',
                                            'plco2an', 'plch4an', 'pln2oan', 'plco2eqa', 'plhgan']].copy()
                plantadjustedvalues_df.replace({"--": pd.NA, "N/A": pd.NA, "": pd.NA}, inplace=True) 
            except Exception: 
                print('Error in PlantAdjustedValues dataframe')

            # PlantEmissionRate
            try: 
                plantemissionrate_df = df[['year', 'orispl', 'plnoxrta', 'plnoxrto', 'plso2rta', 'plco2rta',
                                        'plch4rta', 'pln2orta', 'plc2erta', 'plhgrta', 'plnoxra',
                                        'plnoxro', 'plso2ra', 'plco2ra', 'plch4ra',
                                        'pln2ora', 'plc2era', 'plhgra', 'plnoxcrt', 'plnoxcro',
                                        'plso2crt', 'plco2crt', 'plch4crt', 'pln2ocrt',
                                        'plc2ecrt', 'plhgcrt']].copy()
                plantemissionrate_df.replace({"--": pd.NA, "N/A": pd.NA, "": pd.NA}, inplace=True) 
            except Exception: 
                print('Error in PlantEmissionRate dataframe')

            # PlantFuelTypeGeneration
            try: 
                plantfueltypegeneration_df = df[['year', 'orispl', 'plgenacl', 'plgenaol', 'plgenags',
                                                'plgenanc', 'plgenahy', 'plgenabm', 'plgenawi',
                                                'plgenaso', 'plgenagt', 'plgenaof', 'plgenaop',
                                                'plgenacy', 'plgenacn', 'plgenaco', 'plgenatn', 
                                                'plgenatr', 'plgenato', 'plgenath']].copy()
                plantfueltypegeneration_df.replace({"--": pd.NA, "N/A": pd.NA, "": pd.NA}, inplace=True)
            except Exception: 
                print('Error in PlantFuelTypeGeneration dataframe')
            
            # PlantResourceMix
            try: 
                plantresourcemix_df = df[['year', 'orispl', 'plclpr',
                                        'plolpr', 'plgspr', 'plncpr', 'plhypr', 'plbmpr',
                                        'plwipr', 'plsopr', 'plgtpr', 'plofpr', 'ploppr',
                                        'pltnpr', 'pltrpr', 'pltopr', 'plthpr', 'plcypr',
                                        'plcnpr', 'plcopr']].copy()
                plantresourcemix_df.replace({"--": pd.NA, "N/A": pd.NA, "": pd.NA}, inplace=True)
            except Exception: 
                print('Error in PlantResourceMix dataframe')

            # PlantUnadjustedValues
            try: 
                plantunadjustedvalues_df = df[['year', 'orispl', 'unnox', 'unnoxoz', 'unso2',
                                            'unco2', 'unch4', 'unn2o', 'unco2e', 'unhti',
                                            'unhtioz', 'unhtit', 'unhtiozt', 'bionox', 'bionoxoz',
                                            'bioso2', 'bioco2', 'bioch4', 'bion2o', 'bioco2e',
                                            'chpchti', 'chpchtioz', 'chpnox', 'chpnoxoz', 'chpso2',
                                            'chpco2', 'chpch4', 'chpn2o', 'chpco2e']].copy()
                plantunadjustedvalues_df.replace({"--": pd.NA, "N/A": pd.NA, "": pd.NA}, inplace=True)
            except Exception: 
                print('Error PlantUnadjustedValues dataframe')

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

                    # count to see if table is empty
                    plant_cnt = conn.execute(text("select count(*) from plant;")).scalar()
                
                    plantadjustedvalues_cnt = conn.execute(
                        text("select count(*) from plant_adjusted_values where year = :year"),
                        {"year": int(year)}
                    ).scalar()  

                    plantemissionrate_cnt = conn.execute(
                        text("select count(*) from plant_emission_rate where year = :year"),
                        {"year": int(year)}
                    ).scalar()

                    plantfueltypegeneration_cnt = conn.execute(
                        text("select count(*) from plant_fuel_type_generation where year = :year"),
                        {"year": int(year)}
                    ).scalar()

                    plantresourcemix_cnt = conn.execute(
                        text("select count(*) from plant_resource_mix where year = :year"),
                        {"year": int(year)}
                    ).scalar()

                    plantunadjustedvalues_cnt = conn.execute(
                        text("select count(*) from plant_unadjusted_values where year = :year"),
                        {"year": int(year)}
                    ).scalar()

                    # check count to insert or update the table 
                    if plant_cnt == 0:
                        conn.execute(text("""insert into plant (
                                    pstatabb, fipsst, orispl, utlsrvid, bacode, nerc, 
                                    lat, lon, numunt, numgen, plprmfl, plfuelct, 
                                    oprcode, sector, pname, coalflag, seqplt
                                     ) 
                                    select pstatabb, fipsst, orispl, utlsrvid, bacode, nerc, 
                                            lat, lon, numunt, numgen, plprmfl, plfuelct, 
                                            oprcode, sector, pname, coalflag, seqplt from plant_temp;
                                     """)) 
                    else:
                        conn.execute(text("""
                            update plant set pstatabb = plant_temp.pstatabb, 
                                    fipsst = plant_temp.fipsst, 
                                    utlsrvid = plant_temp.utlsrvid,
                                    bacode = plant_temp.bacode, 
                                    nerc = plant_temp.nerc,  
                                    lat = plant_temp.lat, 
                                    lon = plant_temp.lon, 
                                    numunt = plant_temp.numunt, 
                                    numgen = plant_temp.numgen, 
                                    plprmfl = plant_temp.plprmfl, 
                                    plfuelct = plant_temp.plfuelct, 
                                    oprcode = plant_temp.oprcode, 
                                    sector = plant_temp.sector, 
                                    pname = plant_temp.pname, 
                                    coalflag = plant_temp.coalflag, 
                                    seqplt = plant_temp.seqplt 
                            from plant_temp  
                            where plant.orispl = plant_temp.orispl;
                        """))

                    if plantadjustedvalues_cnt == 0:
                        sql = build_insert_from_temp_sql("plant_adjusted_values", plantadjustedvalues_df)
                        conn.execute(text(sql))  
                    else:
                        sql = update_from_temp_table( "plant_adjusted_values", plantadjustedvalues_df, 'orispl')
                        conn.execute(text(sql))    

                    if plantemissionrate_cnt == 0:
                        sql = build_insert_from_temp_sql("plant_emission_rate", plantemissionrate_df)
                        conn.execute(text(sql))  
                    else:
                        sql = update_from_temp_table("plant_emission_rate", plantemissionrate_df, 'orispl')
                        conn.execute(text(sql))  

                    if plantfueltypegeneration_cnt == 0:
                        sql = build_insert_from_temp_sql("plant_fuel_type_generation", plantfueltypegeneration_df)
                        conn.execute(text(sql))  
                    else:
                        sql = update_from_temp_table("plant_fuel_type_generation", plantfueltypegeneration_df, 'orispl')
                        conn.execute(text(sql)) 

                    if plantresourcemix_cnt == 0:
                        sql = build_insert_from_temp_sql("plant_resource_mix", plantresourcemix_df)
                        conn.execute(text(sql))  
                    else:
                        sql = update_from_temp_table("plant_resource_mix", plantresourcemix_df, 'orispl')
                        conn.execute(text(sql))

                    if plantunadjustedvalues_cnt == 0:
                        sql = build_insert_from_temp_sql("plant_unadjusted_values", plantunadjustedvalues_df)
                        conn.execute(text(sql))  
                    else:
                        sql = update_from_temp_table( "plant_unadjusted_values", plantunadjustedvalues_df, 'orispl')
                        conn.execute(text(sql))   

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

 