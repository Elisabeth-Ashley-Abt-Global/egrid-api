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

            nerc_df = df[['nerc', 'nercname', 'nrnamepcap']] 

            # NercAdjustedValues
            nercadjustedvalues_df = df[['nerc', 'nrhtian', 'nrhtioz', 'nrhtiant', 
                                        'nrhtiozt', 'nrngenan', 'nrngenoz', 'nrngennb', 
                                        'nrnoxan', 'nrnoxoz', 'nrso2an', 'nrco2an', 
                                        'nrch4an', 'nrn2oan', 'nrco2eqa', 'nrhgan', 'year']].copy()
            nercadjustedvalues_df.replace({"--": None, "N/A": None, "": None}, inplace=True)

            # NercEmissionRate
            nercemissionrate_df = df[['nerc', 'nrnoxrta', 'nrnoxrto', 'nrso2rta', 
                                    'nrco2rta', 'nrch4rta', 'nrn2orta', 'nrc2erta', 
                                    'nrhgrta', 'nrnoxra', 'nrnoxro', 'nrso2ra',  
                                    'nrco2ra', 'nrch4ra', 'nrn2ora', 'nrc2era',  
                                    'nrhgra', 'nrnoxcrt', 'nrnoxcro', 'nrso2crt', 
                                    'nrco2crt', 'nrch4crt', 'nrn2ocrt', 'nrc2ecrt', 
                                    'nrhgcrt', 'year']].copy()
            nercemissionrate_df.replace({"--": None, "N/A": None, "": None}, inplace=True)

            #NercFuelTypeEmissionRate
            nercfueltypeemissionrate_df = df[['nerc', 'nrcnoxrt', 'nronoxrt', 'nrgnoxrt', 'nrfsnxrt', 
                                            'nrcnxort', 'nronxort', 'nrgnxort', 'nrfsnort', 
                                            'nrcso2rt', 'nroso2rt', 'nrgso2rt', 'nrfss2rt', 
                                            'nrcco2rt', 'nroco2rt', 'nrgco2rt', 'nrfsc2rt', 
                                            'nrcch4rt', 'nroch4rt', 'nrgch4rt', 'nrfch4rt', 
                                            'nrcn2ort', 'nron2ort', 'nrgn2ort', 'nrfn2ort', 
                                            'nrcc2ert', 'nroc2ert', 'nrgc2ert', 'nrfsc2ert',
                                            'nrchgrt', 'nrfshgrt', 
                                            'nrcnoxr', 'nronoxr', 'nrgnoxr', 'nrfsnxr',
                                            'nrcnxor', 'nronxor', 'nrgnxor', 'nrfsnor',
                                            'nrcso2r', 'nroso2r', 'nrgso2r', 'nrfss2r', 
                                            'nrcco2r', 'nroco2r', 'nrgco2r', 'nrfsc2r',
                                            'nrcch4r', 'nroch4r', 'nrgch4r', 'nrfch4r',
                                            'nrcn2or', 'nron2or', 'nrgn2or', 'nrfn2or', 
                                            'nrcc2er', 'nroc2er', 'nrgc2er',  'nrfsc2er',
                                            'nrchgr', 'nrfshgr', 'year']].copy()
            nercfueltypeemissionrate_df.replace({"--": None, "N/A": None, "": None}, inplace=True)

            #NercFuelTypeGeneration
            nercfueltypegeneration_df = df[['nerc', 'nrgenacl', 'nrgenaol', 'nrgenaso', 'nrgenagt',
                                            'nrgenaof', 'nrgenaop', 'nrgenatn', 'nrgenatr', 
                                            'nrgenato', 'nrgenath', 'nrgenacy', 'nrgenacn',
                                            'nrgenaco', 'nrgenags', 'nrgenanc', 'nrgenahy',
                                            'nrgenabm', 'nrgenawi', 'year']].copy()
            nercfueltypegeneration_df.replace({"--": None, "N/A": None, "": None}, inplace=True)

            #NercNonBaseloadEmissionRate
            nercnonbaseloademissionrate_df = df[['nerc', 'nrnbnox', 'nrnbnxo',
                                                'nrnbso2', 'nrnbco2', 'nrnbch4', 'nrnbn2o',   
                                                'nrnbc2e', 'nrnbhg', 'nrnbgncl', 'nrnbgnol', 'nrnbgngs',  
                                                'nrnbgnnc', 'nrnbgnhy', 'nrnbgnbm', 'nrnbgnwi',  
                                                'nrnbgnso', 'nrnbgngt', 'nrnbgnof', 'nrnbgnop',  
                                                'nrnbclpr', 'nrnbolpr', 'nrnbgspr', 'nrnbncpr',  
                                                'nrnbhypr', 'nrnbbmpr', 'nrnbwipr', 'nrnbsopr',  
                                                'nrnbgtpr', 'nrnbofpr', 'nrnboppr']].copy()
            ### START HERE 4/7/2025 ####

            try:
                nerc_df.to_sql('nerc_temp', con=engine, if_exists='replace', index=False) 
                nercadjustedvalues_df.to_sql('nerc_adjusted_values_temp', con=engine, if_exists='replace', index=False)
                nercemissionrate_df.to_sql('nerc_emission_rate_temp', con=engine, if_exists='replace', index=False)
                nercfueltypeemissionrate_df.to_sql('nerc_emission_rate_temp', con=engine, if_exists='replace', index=False)

                with engine.connect() as conn:
                    trans = conn.begin()
                    conn.execute(text("truncate table nerc cascade;"))  
                    # result = conn.execute(text("SELECT COUNT(*) FROM plant;"))
                   
                    trans.commit() 
                df.to_sql('nerc', con=engine, if_exists='append', index=False)
                print('Success inserting nerc data.')
                return {"success": True, "message": "Data successfully inserted into the NERC table."}
            except Exception as e:
                print('Error inserting nerc data.', e)
                return {"error": str(e)}
              
    except Exception as e:
        logger.error(f"Error while processing R API data: {e}", exc_info=True)
        return {"error": str(e)}
