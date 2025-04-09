# File to communicate with the R API
import requests  
import logging
import pandas as pd  
from sqlalchemy import text 
from .utils import update_from_temp_table, build_insert_from_temp_sql 

logger = logging.getLogger('egrid')
  
def populate_us_data(engine=None, api_url=None):
    print("*populate_us_data")
 
    try:
        response = requests.get(f"{api_url}us")
        data = response.json() 
        # print(data) 
        
        if response.status_code == 200 and data.get('success'):
            us_data = data.get('data', [])
            df = pd.DataFrame(us_data) 

            cast_to_int = ['year']

            # Define the new columns to type cast (2023+ data)
            new_cols = ['usngennb','usgenato','usgenaco','ustopr','uscopr']
            # Define new columns for dataframes (2023+ data)
            new_resource_cols = ['ustopr','uscopr']
            new_ftg_cols = ['usgenato','usgenaco']

            cast_to_float = ['usnamepcap', 'ushtian', 'ushtioz', 'ushtiant', 
                            'ushtiozt', 'usngenan', 'usngenoz', 'usngennb', 'usnoxan', 'usnoxoz', 
                            'usso2an', 'usco2an', 'usch4an', 'usn2oan', 'usco2eqa', 
                            'usnoxrta', 'usnoxrto', 'usso2rta', 'usco2rta', 'usch4rta', 'usn2orta', 'usc2erta',
                            'usnoxra', 'usnoxro', 'usso2ra', 'usco2ra', 'usch4ra', 'usn2ora', 'usc2era',
                            'usnoxcrt', 'usnoxcro', 'usso2crt', 'usco2crt', 'usch4crt', 'usn2ocrt', 'usc2ecrt', 'ushgcrt',
                            'uscnoxrt', 'usonoxrt', 'usgnoxrt', 'usfsnxrt', 'uscnxort', 'usonxort', 'usgnxort', 'usfsnort', 'uscso2rt',
                            'usoso2rt', 'usgso2rt', 'usfss2rt', 'uscco2rt', 'usoco2rt', 'usgco2rt', 'usfsc2rt', 'uscch4rt', 'usoch4rt',
                            'usgch4rt', 'usfch4rt', 'uscn2ort', 'uson2ort', 'usgn2ort', 'usfn2ort', 'uscc2ert', 'usoc2ert', 'usgc2ert',
                            'usfsc2er', 'uscnoxr', 'usonoxr', 'usgnoxr', 'usfsnxr', 'uscnxor', 'usonxor', 'usgnxor', 'usfsnor',
                            'uscso2r', 'usoso2r', 'usgso2r', 'usfss2r', 'uscco2r', 'usoco2r', 'usgco2r', 'usfsc2r', 'uscch4r',
                            'usoch4r', 'usgch4r', 'usfch4r', 'uscn2or', 'uson2or', 'usgn2or', 'usfn2or', 'uscc2er', 'usoc2er',
                            'usgc2er', 'usfsc2er', 'usgenacl', 'usgenaol', 'usgenaso', 'usgenagt', 'usgenaof', 'usgenaop', 'usgenatn', 'usgenatr', 
                            'usgenato', 'usgenath', 'usgenacy', 'usgenacn', 'usgenaco', 'usgenags', 'usgenanc', 'usgenahy',
                            'usgenabm', 'usgenawi', 'usnbnox', 'usnbnxo', 'usnbso2', 'usnbco2', 'usnbch4', 'usnbn2o',   
                            'usnbc2e', 'usnbgncl', 'usnbgnol', 'usnbgngs', 'usnbgnnc', 'usnbgnhy', 'usnbgnbm', 'usnbgnwi',  
                            'usnbgnso', 'usnbgngt', 'usnbgnof', 'usnbgnop', 'usnbclpr', 'usnbolpr', 'usnbgspr', 'usnbncpr',  
                            'usnbhypr', 'usnbbmpr', 'usnbwipr', 'usnbsopr', 'usnbgtpr', 'usnbofpr', 'usnboppr', 'usclpr',
                            'usolpr', 'usgspr', 'usncpr', 'ushypr', 'usbmpr', 'uswipr', 'ussopr', 'usgtpr', 
                            'usofpr', 'usoppr', 'ustnpr', 'ustrpr', 'ustopr', 'usthpr', 'uscypr', 'uscnpr', 'uscopr']
            
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
            # US
            us_df = df[['usnamepcap']] 

            # UsAdjustedValues
            try: 
                usadjustedvalues_df = df[['year', 'usnamepcap', 'ushtian', 'ushtioz', 
                                          'ushtiant', 'ushtiozt', 'usngenan', 'usngenoz', 
                                          'usnoxan', 'usnoxoz', 'usso2an', 'usco2an', 
                                          'usch4an', 'usn2oan', 'usco2eqa', 'ushgan']].copy()
                if year >= 2023: 
                    # add 'bangennb' column to baadjustedvalues_df for records from 2023 onward
                    usadjustedvalues_df['usngennb'] = df['usngennb']
                
                usadjustedvalues_df.copy()
                usadjustedvalues_df.replace({"--": None, "N/A": None, "": None}, inplace=True) # replace placeholders else you'll encounter  invalid input syntax for type double precision
            except Exception: 
                print('Error in UsAdjustedValues dataframe')

            # UsEmissionRate
            try:  
                usemissionrate_df = df[['year', 'usnamepcap', 'usnoxrta','usnoxrto',
                                        'usso2rta', 'usco2rta', 'usch4rta', 'usn2orta',
                                        'usc2erta', 'ushgrta', 'usnoxra', 'usnoxro',
                                        'usso2ra', 'usco2ra', 'usch4ra', 'usn2ora', 
                                        'usc2era', 'ushgra', 'usnoxcrt', 'usnoxcro', 
                                        'usso2crt', 'usco2crt', 'usch4crt', 'usn2ocrt', 
                                        'ushgcrt', 'usc2ecrt']].copy() 
                usemissionrate_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception:
                print('Error in UsEmissionRate dataframe')

            # UsFuelTypeEmissionRate
            try: 
                usfueltypeemissionrate_df = df[['year', 'usnamepcap', 'uscnoxrt', 'usonoxrt', 'usgnoxrt', 'usfsnxrt', 
                                                'uscnxort', 'usonxort', 'usgnxort', 'usfsnort', 
                                                'uscso2rt', 'usoso2rt', 'usgso2rt', 'usfss2rt', 
                                                'uscco2rt', 'usoco2rt', 'usgco2rt', 'usfsc2rt', 
                                                'uscch4rt', 'usoch4rt', 'usgch4rt', 'usfch4rt', 
                                                'uscn2ort', 'uson2ort', 'usgn2ort', 'usfn2ort', 
                                                'uscc2ert', 'usoc2ert', 'usgc2ert', 'usfsc2ert',
                                                'uschgrt', 'usfshgrt', 'uscnoxr', 'usonoxr', 
                                                'usgnoxr', 'usfsnxr', 'uscnxor', 'usonxor', 
                                                'usgnxor', 'usfsnor', 'uscso2r', 'usoso2r', 
                                                'usgso2r', 'usfss2r', 'uscco2r', 'usoco2r', 
                                                'usgco2r', 'usfsc2r', 'uscch4r', 'usoch4r', 
                                                'usgch4r', 'usfch4r', 'uscn2or', 'uson2or', 
                                                'usgn2or', 'usfn2or', 'uscc2er', 'usoc2er', 
                                                'usgc2er',  'usfsc2er', 'uschgr', 'usfshgr']].copy()
                usfueltypeemissionrate_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in UsFuelTypeEmissionRate dataframe')

            # UsFuelTypeGeneration
            try: 
                usfueltypegeneration_df = df[['year', 'usnamepcap', 'usgenacl', 'usgenaol', 'usgenaso', 'usgenagt',
                                            'usgenaof', 'usgenaop', 'usgenatn', 'usgenatr', 
                                            'usgenath', 'usgenacy', 'usgenacn',
                                            'usgenags', 'usgenanc', 'usgenahy',
                                            'usgenabm', 'usgenawi']].copy()
                if year >= 2023: 
                    for col in new_ftg_cols: 
                        usfueltypegeneration_df[col] = df[col]

                usfueltypegeneration_df.copy()
                usfueltypegeneration_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in UsFuelTypeGeneration dataframe')

            # UsNonBaseloadValues
            try:
                usnonbaseloadvalues_df = df[['year', 'usnamepcap', 'usnbnox', 'usnbnxo',
                                            'usnbso2', 'usnbco2', 'usnbch4', 'usnbn2o',   
                                            'usnbc2e', 'usnbhg', 'usnbgncl', 'usnbgnol', 'usnbgngs',  
                                            'usnbgnnc', 'usnbgnhy', 'usnbgnbm', 'usnbgnwi',  
                                            'usnbgnso', 'usnbgngt', 'usnbgnof', 'usnbgnop',  
                                            'usnbclpr', 'usnbolpr', 'usnbgspr', 'usnbncpr',  
                                            'usnbhypr', 'usnbbmpr', 'usnbwipr', 'usnbsopr',  
                                            'usnbgtpr', 'usnbofpr', 'usnboppr']].copy()
                usnonbaseloadvalues_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in UsNonBaseloadValues dataframe')

            # UsResourceMix
            try: 
                usresourcemix_df = df[['year', 'usnamepcap', 'usclpr', 'usolpr', 'usgspr', 
                                        'usncpr', 'ushypr', 'usbmpr', 'uswipr', 
                                        'ussopr', 'usgtpr', 'usofpr', 'usoppr', 
                                        'ustnpr', 'ustrpr', 'usthpr', 
                                        'uscypr', 'uscnpr']].copy()
                if year >= 2023: 
                    for col in new_resource_cols: 
                        usresourcemix_df[col] = df[col]

                usresourcemix_df.copy()
                usresourcemix_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in UsResourceMix dataframe')

            try:
                # build temp tables, replace will replace the table if it already exists
                us_df.to_sql('us_temp', con=engine, if_exists='replace', index=False) 
                usadjustedvalues_df.to_sql('us_adjusted_values_temp', con=engine, if_exists='replace', index=False)
                usemissionrate_df.to_sql('us_emission_rate_temp', con=engine, if_exists='replace', index=False)
                usfueltypeemissionrate_df.to_sql('us_fuel_type_emission_rate_temp', con=engine, if_exists='replace', index=False)
                usfueltypegeneration_df.to_sql('us_fuel_type_generation_temp', con=engine, if_exists='replace', index=False)
                usnonbaseloadvalues_df.to_sql('us_nonbaseload_values_temp', con=engine, if_exists='replace', index=False)
                usresourcemix_df.to_sql('us_resource_mix_temp', con=engine, if_exists='replace', index=False)

                with engine.connect() as conn:
                    trans = conn.begin()
                    us_cnt = conn.execute(text("select count(*) from us;")).scalar()
                    
                    # count to see if table is empty
                    usadjustedvalues_cnt = conn.execute(
                        text("select count(*) from us_adjusted_values where year = :year"),
                        {"year": int(year)}
                    ).scalar()  

                    usemissionrate_cnt = conn.execute(
                        text("select count(*) from us_emission_rate where year = :year"),
                        {"year": int(year)}
                    ).scalar()

                    usfueltypeemissionrate_cnt = conn.execute(
                        text("select count(*) from us_fuel_type_emission_rate where year = :year"),
                        {"year": int(year)}
                    ).scalar()

                    usfueltypegeneration_cnt = conn.execute(
                        text("select count(*) from us_fuel_type_generation where year = :year"),
                        {"year": int(year)}
                    ).scalar()

                    usnonbaseloadvalues_cnt = conn.execute(
                        text("select count(*) from us_nonbaseload_values where year = :year"),
                        {"year": int(year)}
                    ).scalar()

                    usresourcemix_cnt = conn.execute(
                        text("select count(*) from us_resource_mix where year = :year"),
                        {"year": int(year)}
                    ).scalar()

                    # check count to insert or update the table
                    if us_cnt == 0:
                        conn.execute(text("""
                            insert into us (
                                year, usnamepcap
                            ) select year, usnamepcap
                            from us_temp;
                        """))  
                    else:
                        conn.execute(text("""
                            update us
                            set year = ust.year, 
                                usnamepcap = ust.usnamepcap              
                            from us_temp ust
                            where us.year = ust.year
                                and us.usnamepcap = ust.usnamepcap;
                        """)) 

                    if usadjustedvalues_cnt == 0:
                        sql = build_insert_from_temp_sql("us_adjusted_values", usadjustedvalues_df)
                        conn.execute(text(sql))  
                    else:
                        sql = update_from_temp_table( "us_adjusted_values", usadjustedvalues_df, "usnamepcap")
                        conn.execute(text(sql))    

                    if usemissionrate_cnt == 0:
                        sql = build_insert_from_temp_sql("us_emission_rate", usemissionrate_df)
                        conn.execute(text(sql))  
                    else:
                        sql = update_from_temp_table("us_emission_rate", usemissionrate_df, "usnamepcap")
                        conn.execute(text(sql))  

                    if usfueltypeemissionrate_cnt == 0:
                        sql = build_insert_from_temp_sql("us_fuel_type_emission_rate", usfueltypeemissionrate_df)
                        conn.execute(text(sql))  
                    else:
                        sql = update_from_temp_table("us_fuel_type_emission_rate", usfueltypeemissionrate_df, "usnamepcap")
                        conn.execute(text(sql)) 

                    if usfueltypegeneration_cnt == 0:
                        sql = build_insert_from_temp_sql("us_fuel_type_generation", usfueltypegeneration_df)
                        conn.execute(text(sql))  
                    else:
                        sql = update_from_temp_table("us_fuel_type_generation", usfueltypegeneration_df, "usnamepcap")
                        conn.execute(text(sql)) 

                    if usnonbaseloadvalues_cnt == 0:
                        sql = build_insert_from_temp_sql("us_nonbaseload_values", usnonbaseloadvalues_df)
                        conn.execute(text(sql))  
                    else:
                        sql = update_from_temp_table("us_nonbaseload_values", usnonbaseloadvalues_df, "usnamepcap")
                        conn.execute(text(sql)) 

                    if usresourcemix_cnt == 0:
                        sql = build_insert_from_temp_sql("us_resource_mix", usresourcemix_df)
                        conn.execute(text(sql))  
                    else:
                        sql = update_from_temp_table("us_resource_mix", usresourcemix_df, "usnamepcap")
                        conn.execute(text(sql)) 

                    # drop temp tables
                    conn.execute(text("drop table us_temp;"))
                    conn.execute(text("drop table us_adjusted_values_temp;")) 
                    conn.execute(text("drop table us_emission_rate_temp;"))
                    conn.execute(text("drop table us_fuel_type_emission_rate_temp"))
                    conn.execute(text("drop table us_fuel_type_generation_temp"))
                    conn.execute(text("drop table us_nonbaseload_values_temp"))
                    conn.execute(text("drop table us_resource_mix_temp"))
                    trans.commit() 

                print('Success populating US data.')  
                  
            except Exception as e:
                print('Error populating US data.', e)
                return {"error": str(e)}  

            return {"success": True, "message": "Data successfully inserted into the US table."}
        else:
            return {"error": f"Failed to connect to R API with status code {response.status_code}"}
    
    except Exception as e:
        return {"error": str(e)}