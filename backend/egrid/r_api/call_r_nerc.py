import requests
from egrid.models import NercRegion
from sqlalchemy import text 
import requests 
import logging 
import pandas as pd 

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

            #NercFuelTypeEmissionRate
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

            #NercFuelTypeGeneration
            try: 
                nercfueltypegeneration_df = df[['nerc', 'nrgenacl', 'nrgenaol', 'nrgenaso', 'nrgenagt',
                                                'nrgenaof', 'nrgenaop', 'nrgenatn', 'nrgenatr', 
                                                'nrgenato', 'nrgenath', 'nrgenacy', 'nrgenacn',
                                                'nrgenaco', 'nrgenags', 'nrgenanc', 'nrgenahy',
                                                'nrgenabm', 'nrgenawi', 'year']].copy()
                nercfueltypegeneration_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in NercFuelTypeGeneration dataframe')

            #NercNonBaseloadEmissionRate
            try:
                nercnonbaseloademissionrate_df = df[['nerc', 'nrnbnox', 'nrnbnxo',
                                                    'nrnbso2', 'nrnbco2', 'nrnbch4', 'nrnbn2o',   
                                                    'nrnbc2e', 'nrnbhg', 'nrnbgncl', 'nrnbgnol', 'nrnbgngs',  
                                                    'nrnbgnnc', 'nrnbgnhy', 'nrnbgnbm', 'nrnbgnwi',  
                                                    'nrnbgnso', 'nrnbgngt', 'nrnbgnof', 'nrnbgnop',  
                                                    'nrnbclpr', 'nrnbolpr', 'nrnbgspr', 'nrnbncpr',  
                                                    'nrnbhypr', 'nrnbbmpr', 'nrnbwipr', 'nrnbsopr',  
                                                    'nrnbgtpr', 'nrnbofpr', 'nrnboppr']].copy()
                nercnonbaseloademissionrate_df.replace({"--": None, "N/A": None, "": None}, inplace=True)
            except Exception: 
                print('Error in NercNonBaseloadEmissionRate dataframe')

            #NercResourceMix
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
                nerc_df.to_sql('nerc_temp', con=engine, if_exists='replace', index=False) 
                nercadjustedvalues_df.to_sql('nerc_adjusted_values_temp', con=engine, if_exists='replace', index=False)
                nercemissionrate_df.to_sql('nerc_emission_rate_temp', con=engine, if_exists='replace', index=False)
                nercfueltypeemissionrate_df.to_sql('nerc_fuel_type_emission_rate_temp', con=engine, if_exists='replace', index=False)
                nercfueltypegeneration_df.to_sql('nerc_fuel_type_generation_temp', con=engine, if_exists='replace', index=False)
                nercnonbaseloademissionrate_df.to_sql('nerc_nonbaseload_emission_rate_temp', con=engine, if_exists='replace', index=False)
                nercresourcemix_df.to_sql('nerc_resource_mix_temp', con=engine, if_exists='replace', index=False)

                with engine.connect() as conn:
                    trans = conn.begin()

                    nerc_cnt = conn.execute(text("select count(*) from nerc;")).scalar()
                    nercadjustedvalues_cnt = conn.execute(
                        text("select count(*) from nerc_adjusted_values where year = :year"),
                        {"year": year}
                    ).scalar() 
                    nercemissionrate_cnt = conn.execute(
                        text("select count(*) from nerc_emission_rate where year = :year"),
                        {"year": year}
                    ).scalar() 
                    nercfueltypeemissionrate_cnt = conn.execute(
                        text("select count(*) from nerc_fuel_type_emission_rate where year = :year"),
                        {"year": year}
                    ).scalar() 
                    nercfueltypegeneration_cnt = conn.execute(
                        text("select count(*) from nerc_fuel_type_generation where year = :year"),
                        {"year": year}
                    ).scalar() 
                    nercnonbaseloademissionrate_cnt = conn.execute(
                        text("select count(*) from nerc_nonbaseload_emission_rate where year = :year"),
                        {"year": year}
                    ).scalar() 
                    nercresourcemix_cnt = conn.execute(
                        text("select count(*) from nerc_resource_mix where year = :year"),
                        {"year": year}
                    ).scalar() 

                    if nerc_cnt == 0:   
                        conn.execute(text("""
                            insert into nerc (
                                nerc, nercname, nrnamepcap
                            ) select nerc, nercname, nrnamepcap from nerc_temp;
                        """))  
                    else:
                        conn.execute(text("""
                            update nerc
                            set nerc = nerc_temp.nerc, 
                                nercname = nerc_temp.nercname,
                                nrnamepcap = nerc_temp.nrnamepcap
                            from nerc_temp  
                            where nerc.nerc = nerc_temp.nerc;
                        """))

                    if nercadjustedvalues_cnt == 0:
                        conn.execute(text("""
                            insert into nerc_adjusted_values (
                                nerc, nrhtian, nrhtioz, nrhtiant, 
                                nrhtiozt, nrngenan, nrngenoz, nrngennb, 
                                nrnoxan, nrnoxoz, nrso2an, nrco2an, 
                                nrch4an, nrn2oan, nrco2eqa, nrhgan, year
                            ) select nerc, nrhtian, nrhtioz, nrhtiant, 
                                nrhtiozt, nrngenan, nrngenoz, nrngennb, 
                                nrnoxan, nrnoxoz, nrso2an, nrco2an, 
                                nrch4an, nrn2oan, nrco2eqa, nrhgan, year
                            from nerc_adjusted_values_temp;
                        """))
                    else:   
                        conn.execute(text("""  
                            update nerc_adjusted_values
                            set nerc = nerc_adjusted_values_temp.nerc,
                                nrhtian = nerc_adjusted_values_temp.nrhtian, 
                                nrhtioz = nerc_adjusted_values_temp.nrhtioz, 
                                nrhtiant = nerc_adjusted_values_temp.nrhtiant, 
                                nrhtiozt = nerc_adjusted_values_temp.nrhtiozt, 
                                nrngenan = nerc_adjusted_values_temp.nrngenan,
                                nrngenoz = nerc_adjusted_values_temp.nrngenoz, 
                                nrngennb = nerc_adjusted_values_temp.nrngennb, 
                                nrnoxan = nerc_adjusted_values_temp.nrnoxan, 
                                nrnoxoz = nerc_adjusted_values_temp.nrnoxoz, 
                                nrso2an = nerc_adjusted_values_temp.nrso2an, 
                                nrco2an = nerc_adjusted_values_temp.nrco2an, 
                                nrch4an = nerc_adjusted_values_temp.nrch4an, 
                                nrn2oan = nerc_adjusted_values_temp.nrn2oan, 
                                nrco2eqa = nerc_adjusted_values_temp.nrco2eqa, 
                                nrhgan = nerc_adjusted_values_temp.nrhgan, 
                                year = nerc_adjusted_values_temp.year
                            from nerc_adjusted_values_temp 
                            where nerc_adjusted_values.nerc = nerc_adjusted_values_temp.nerc 
                                and nerc_adjusted_values.year = nerc_adjusted_values_temp.year;
                        """))

                    if nercemissionrate_cnt == 0:
                        conn.execute(text("""
                            insert into nerc_emission_rate (
                                nerc, nrnoxrta, nrnoxrto, nrso2rta, 
                                nrco2rta, nrch4rta, nrn2orta, nrc2erta, 
                                nrhgrta, nrnoxra, nrnoxro, nrso2ra,  
                                nrco2ra, nrch4ra, nrn2ora, nrc2era,  
                                nrhgra, nrnoxcrt, nrnoxcro, nrso2crt, 
                                nrco2crt, nrch4crt, nrn2ocrt, nrc2ecrt, 
                                nrhgcrt, year
                            ) select nerc, nrnoxrta, nrnoxrto, nrso2rta, 
                                nrco2rta, nrch4rta, nrn2orta, nrc2erta, 
                                nrhgrta, nrnoxra, nrnoxro, nrso2ra,  
                                nrco2ra, nrch4ra, nrn2ora, nrc2era,  
                                nrhgra, nrnoxcrt, nrnoxcro, nrso2crt, 
                                nrco2crt, nrch4crt, nrn2ocrt, nrc2ecrt, 
                                nrhgcrt, year
                            from nerc_emission_rate_temp;
                        """))
                    else:   
                        conn.execute(text("""  
                            update nerc_adjusted_values
                            set nerc = nerc_, 
                                nrnoxrta, 
                                nrnoxrto, 
                                nrso2rta, 
                                nrco2rta, 
                                nrch4rta, 
                                nrn2orta, 
                                nrc2erta, 
                                nrhgrta, 
                                nrnoxra,
                                nrnoxro, 
                                nrso2ra,  
                                nrco2ra, 
                                nrch4ra, 
                                nrn2ora, 
                                nrc2era,  
                                nrhgra, 
                                nrnoxcrt, 
                                nrnoxcro, 
                                nrso2crt, 
                                nrco2crt, 
                                nrch4crt, 
                                nrn2ocrt, 
                                nrc2ecrt, 
                                nrhgcrt, 
                                year
                            from nerc_emission_rate_temp 
                            where nerc_emission_rate.nerc = nerc_emission_rate_temp.nerc 
                                and nerc_emission_rate.year = nerc_emission_rate_temp.year;
                        """))
  
                    conn.execute(text("drop table nerc_temp;"))
                    conn.execute(text("drop table nerc_adjusted_values_temp;"))
 
                    trans.commit() 
 
                print('success')
                return {"success": True, "message": "Data successfully inserted into the NERC table."}
            except Exception as e:
                print('error', e)
                return {"error": str(e)}
        else:
            print('error')
            return {"error": "R API returned an error: {}".format(data.get('error'))} 
    except Exception as e:
        return {"error": str(e)}