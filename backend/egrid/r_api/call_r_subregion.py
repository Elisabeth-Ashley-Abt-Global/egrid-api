# File to communicate with the R API
import requests  
import logging
import pandas as pd  
from sqlalchemy import text 
from .utils import update_from_temp_table, build_insert_from_temp_sql 


logger = logging.getLogger('egrid')
 
def populate_state_data(engine=None, api_url=None): 
    print('populate_subregion_data')
    logger.debug("*populate_subregion_data")

    try:
        response = requests.get(f"{api_url}subrgn")
        data = response.json() 
        
        if response.status_code == 200 and data.get('success'):
            subregion_data = data.get('data', [])
            df = pd.DataFrame(subregion_data)
        
            cast_to_int = ['year']
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

            for col in cast_to_int:
                df[col] = pd.to_numeric(df[col], errors='coerce').astype(int)

            for col in cast_to_float:
                df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)

            year = df['year'].unique()[0] 
            print('year ', year)

            # create tables 
            # Subregion
            subregion_df = df[['subrgn', 'srname', 'srnamepcap']].copy() 

            # SubrgnAdjustedValues
            try: 
                subrgnadjustedvalues_df = df[['subrgn', 'srhtian', 'srhtioz', 'srhtiant', 
                                            'srhtiozt', 'srngenan', 'srngenoz', 'srngennb', 
                                            'srnoxan', 'srnoxoz', 'srso2an', 'srco2an', 
                                            'srch4an', 'srn2oan', 'srco2eqa', 'srhgan', 'year']].copy()
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
                                                'srgenato', 'srgenath', 'srgenacy', 'srgenacn',
                                                'srgenaco', 'srgenags', 'srgenanc', 'srgenahy',
                                                'srgenabm', 'srgenawi', 'year']].copy()
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
                                        'srtnpr', 'srtrpr', 'srtopr', 'srthpr', 
                                        'srcypr', 'srcnpr', 'srcopr']].copy()
                subrgnresourcemix_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in SubrgnResourceMix dataframe')

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
                    
                    # count to see if table is empty
                    subregion_cnt = conn.execute(text("select count(*) from subregion;")).scalar()

                    subrgnadjustedvalues_cnt = conn.execute(
                        text("select count(*) from subrgn_adjusted_values where year = :year"),
                        {"year": int(year)}
                    ).scalar()  

                    subrgnemissionrate_cnt = conn.execute(
                        text("select count(*) from subrgn_emission_rate where year = :year"),
                        {"year": int(year)}
                    ).scalar()

                    subrgnfueltypeemissionrate_cnt = conn.execute(
                        text("select count(*) from subrgn_fuel_type_emission_rate where year = :year"),
                        {"year": int(year)}
                    ).scalar()

                    subrgnfueltypegeneration_cnt = conn.execute(
                        text("select count(*) from subrgn_fuel_type_generation where year = :year"),
                        {"year": int(year)}
                    ).scalar()

                    subrgnnonbaseloadvalues_cnt = conn.execute(
                        text("select count(*) from subrgn_nonbaseload_values where year = :year"),
                        {"year": int(year)}
                    ).scalar()

                    subrgnresourcemix_cnt = conn.execute(
                        text("select count(*) from subrgn_resource_mix where year = :year"),
                        {"year": int(year)}
                    ).scalar()

                    # check count to insert or update the table
                    if subregion_cnt == 0:
                        conn.execute(text("""
                            insert into state (
                                subrgn, srname, srnamepcap
                            ) select subrgn, srname, srnamepcap
                            from subregion_temp;
                        """))  
                    else:
                        conn.execute(text("""
                            update subregion
                            set subrgn = subregion_temp.subrgn, 
                                srname = subregion_temp.srname,
                                srnamepcap = subregion_temp.srnamepcap              
                            from subregion_temp
                            where subregion.subrgn = subrgn_temp.subrgn;
                        """))  

                    if subrgnadjustedvalues_cnt == 0:
                        sql = build_insert_from_temp_sql("subrgn_adjusted_values", subrgnadjustedvalues_df)
                        conn.execute(text(sql))  
                    else:
                        sql = update_from_temp_table( "subrgn_adjusted_values", subrgnadjustedvalues_df)
                        conn.execute(text(sql))    

                    if subrgnemissionrate_cnt == 0:
                        sql = build_insert_from_temp_sql("subrgn_emission_rate", subrgnemissionrate_df)
                        conn.execute(text(sql))  
                    else:
                        sql = update_from_temp_table("subrgn_emission_rate", subrgnemissionrate_df)
                        conn.execute(text(sql))  

                    if subrgnfueltypeemissionrate_cnt == 0:
                        sql = build_insert_from_temp_sql("subrgn_fuel_type_emission_rate", subrgnfueltypeemissionrate_df)
                        conn.execute(text(sql))  
                    else:
                        sql = update_from_temp_table("subrgn_fuel_type_emission_rate", subrgnfueltypeemissionrate_df)
                        conn.execute(text(sql)) 

                    if subrgnfueltypegeneration_cnt == 0:
                        sql = build_insert_from_temp_sql("subrgn_fuel_type_generation", subrgnfueltypegeneration_df)
                        conn.execute(text(sql))  
                    else:
                        sql = update_from_temp_table("subrgn_fuel_type_generation", subrgnfueltypegeneration_df)
                        conn.execute(text(sql)) 

                    if subrgnnonbaseloadvalues_cnt == 0:
                        sql = build_insert_from_temp_sql("subrgn_nonbaseload_values", subrgnnonbaseloadvalues_df)
                        conn.execute(text(sql))  
                    else:
                        sql = update_from_temp_table("subrgn_nonbaseload_values", subrgnnonbaseloadvalues_df)
                        conn.execute(text(sql)) 

                    if subrgnresourcemix_cnt == 0:
                        sql = build_insert_from_temp_sql("subrgn_resource_mix", subrgnresourcemix_df)
                        conn.execute(text(sql))  
                    else:
                        sql = update_from_temp_table("subrgn_resource_mix", subrgnresourcemix_df)
                        conn.execute(text(sql)) 

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