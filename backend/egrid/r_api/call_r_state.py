import requests
from egrid.models import (
    State, 
    StateAnnualCombustion, 
    StateEmissionRate, 
    StateFuelTypeEmissionRate,
    StateFuelTypeGeneration,
    StateNonBaseloadEmissionRate
)

import requests 
import logging

logger = logging.getLogger('egrid')


def sanitize_numeric(value):
    try:
        return float(value)  # Convert to a float or int
    except (ValueError, TypeError):
        return None  # Return None for invalid values

def call_r_state():
    try:
        logger.debug('calling r state')
        response = requests.get("http://127.0.0.1:8001/state")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                state_data = data.get('data', [])
                # logger.debug('state_data is: ', state_data)
                if not state_data:
                    logger.debug("R API returned no data. Skipping database update.")
                    return {"success": False, "message": "R API returned no data."}

                for item in state_data:
                    state, created = State.objects.update_or_create(
                        fipsst=item.get('fipsst'), 
                        defaults={
                            'pstatabb':item.get('pstatabb'), 
                        }
                    ) 

                    if created:
                        logger.info(f"Inserted new plant: {state.fipsst}")
                    else:
                        logger.info(f"Updated existing plant: {state.fipsst}")

                    StateAnnualCombustion.objects.update_or_create(
                        fipsst=State.objects.get(fipsst=item.get('fipsst')),
                        defaults={
                            'sthtian':sanitize_numeric(item.get('sthtian')),  
                            'sthtioz':sanitize_numeric(item.get('sthtioz')),   
                            'sthtiant':sanitize_numeric(item.get('sthtiant')),
                            'sthtiozt':sanitize_numeric(item.get('sthtiozt')),
                            'stngenan':sanitize_numeric(item.get('stngenan')),
                            'stngenoz':sanitize_numeric(item.get('stngenoz')),
                            'stnoxan':sanitize_numeric(item.get('stnoxan')),
                            'stnoxoz':sanitize_numeric(item.get('stnoxoz')),
                            'stso2an':sanitize_numeric(item.get('stso2an')),
                            'stco2an':sanitize_numeric(item.get('stco2an')),
                            'stch4an':sanitize_numeric(item.get('stch4an')),
                            'stn2oan':sanitize_numeric(item.get('stn2oan')),
                            'stco2eqa':sanitize_numeric(item.get('stco2eqa')),
                            'sthgan':sanitize_numeric(item.get('sthgan')),
                            'year':sanitize_numeric(item.get('year'))
                        }
                    )

                    StateEmissionRate.objects.update_or_create(
                        fipsst=State.objects.get(fipsst=item.get('fipsst')),
                        defaults={ 
                            'stnoxrta':sanitize_numeric(item.get('stnoxrta')),
                            'stnoxrto':sanitize_numeric(item.get('stnoxrto')),
                            'stso2rta':sanitize_numeric(item.get('stso2rta')),
                            'stco2rta':sanitize_numeric(item.get('stco2rta')),
                            'stch4rta':sanitize_numeric(item.get('stch4rta')),
                            'stn2orta':sanitize_numeric(item.get('stn2orta')),
                            'stc2erta':sanitize_numeric(item.get('stc2erta')),
                            'sthgrta':sanitize_numeric(item.get('sthgrta')),
                            'stnoxra':sanitize_numeric(item.get('stnoxra')),
                            'stnoxro':sanitize_numeric(item.get('stnoxro')),
                            'stso2ra':sanitize_numeric(item.get('stso2ra')),
                            'stco2ra':sanitize_numeric(item.get('stco2ra')),
                            'stch4ra':sanitize_numeric(item.get('stch4ra')),
                            'stn2ora':sanitize_numeric(item.get('stn2ora')),
                            'stc2era':sanitize_numeric(item.get('stc2era')),
                            'sthgra':sanitize_numeric(item.get('sthgra')),
                            'stnoxcrt':sanitize_numeric(item.get('stnoxcrt')),
                            'stnoxcro':sanitize_numeric(item.get('stnoxcro')),
                            'stso2crt':sanitize_numeric(item.get('stso2crt')),
                            'stco2crt':sanitize_numeric(item.get('stco2crt')),
                            'stch4crt':sanitize_numeric(item.get('stch4crt')),
                            'stn2ocrt':sanitize_numeric(item.get('stn2ocrt')),
                            'stc2ecrt':sanitize_numeric(item.get('stc2ecrt')),
                            'sthgcrt':sanitize_numeric(item.get('sthgcrt')),
                            'year':sanitize_numeric(item.get('year')) 
                        }
                    )

                    StateFuelTypeEmissionRate.objects.update_or_create(
                        fipsst=State.objects.get(fipsst=item.get('fipsst')),
                        defaults={ 
                            'stcnoxrt':sanitize_numeric(item.get('stcnoxrt')),
                            'stonoxrt':sanitize_numeric(item.get('stonoxrt')), 
                            'stgnoxrt':sanitize_numeric(item.get('stgnoxrt')), 
                            'stfsnxrt':sanitize_numeric(item.get('stfsnxrt')), 
                            'stcnxort':sanitize_numeric(item.get('stcnxort')), 
                            'stonxort':sanitize_numeric(item.get('stonxort')), 
                            'stgnxort':sanitize_numeric(item.get('stgnxort')), 
                            'stfsnort':sanitize_numeric(item.get('stfsnort')), 
                            'stcso2rt':sanitize_numeric(item.get('stcso2rt')), 
                            'stoso2rt':sanitize_numeric(item.get('stoso2rt')), 
                            'stgso2rt':sanitize_numeric(item.get('stgso2rt')), 
                            'stfss2rt':sanitize_numeric(item.get('stfss2rt')), 
                            'stcco2rt':sanitize_numeric(item.get('stcco2rt')), 
                            'stoco2rt':sanitize_numeric(item.get('stoco2rt')), 
                            'stgco2rt':sanitize_numeric(item.get('stgco2rt')), 
                            'stfsc2rt':sanitize_numeric(item.get('stfsc2rt')), 
                            'stcch4rt':sanitize_numeric(item.get('stcch4rt')), 
                            'stoch4rt':sanitize_numeric(item.get('stoch4rt')), 
                            'stgch4rt':sanitize_numeric(item.get('stgch4rt')), 
                            'stfch4rt':sanitize_numeric(item.get('stfch4rt')), 
                            'stcn2ort':sanitize_numeric(item.get('stcn2ort')), 
                            'ston2ort':sanitize_numeric(item.get('ston2ort')), 
                            'stgn2ort':sanitize_numeric(item.get('stgn2ort')), 
                            'stfn2ort':sanitize_numeric(item.get('stfn2ort')), 
                            'stcc2ert':sanitize_numeric(item.get('stcc2ert')), 
                            'stoc2ert':sanitize_numeric(item.get('stoc2ert')), 
                            'stgc2ert':sanitize_numeric(item.get('stgc2ert')), 
                            'stfsc2ert':sanitize_numeric(item.get('stfsc2ert')),
                            'stchgrt':sanitize_numeric(item.get('stchgrt')),
                            'stfshgrt':sanitize_numeric(item.get('stfshgrt')),
                            'stcnoxr':sanitize_numeric(item.get('stcnoxr')),  
                            'stonoxr':sanitize_numeric(item.get('stonoxr')),  
                            'stgnoxr':sanitize_numeric(item.get('stgnoxr')),  
                            'stfsnxr':sanitize_numeric(item.get('stfsnxr')),  
                            'stcnxor':sanitize_numeric(item.get('stcnxor')),  
                            'stonxor':sanitize_numeric(item.get('stonxor')),  
                            'stgnxor':sanitize_numeric(item.get('stgnxor')),  
                            'stfsnor':sanitize_numeric(item.get('stfsnor')),  
                            'stcso2r':sanitize_numeric(item.get('stcso2r')),  
                            'stoso2r':sanitize_numeric(item.get('stoso2r')),  
                            'stgso2r':sanitize_numeric(item.get('stgso2r')),  
                            'stfss2r':sanitize_numeric(item.get('stfss2r')),  
                            'stcco2r':sanitize_numeric(item.get('stcco2r')),  
                            'stoco2r':sanitize_numeric(item.get('stoco2r')),  
                            'stgco2r':sanitize_numeric(item.get('stgco2r')),  
                            'stfsc2r':sanitize_numeric(item.get('stfsc2r')),  
                            'stcch4r':sanitize_numeric(item.get('stcch4r')),  
                            'stoch4r':sanitize_numeric(item.get('stoch4r')),  
                            'stgch4r':sanitize_numeric(item.get('stgch4r')),  
                            'stfch4r':sanitize_numeric(item.get('stfch4r')),  
                            'stcn2or':sanitize_numeric(item.get('stcn2or')),  
                            'ston2or':sanitize_numeric(item.get('ston2or')),  
                            'stgn2or':sanitize_numeric(item.get('stgn2or')),  
                            'stfn2or':sanitize_numeric(item.get('stfn2or')),  
                            'stcc2er':sanitize_numeric(item.get('stcc2er')),  
                            'stoc2er':sanitize_numeric(item.get('stoc2er')),  
                            'stgc2er':sanitize_numeric(item.get('stgc2er')),  
                            'stfsc2er':sanitize_numeric(item.get('stfsc2er')), 
                            'stchgr':sanitize_numeric(item.get('stchgr')),
                            'stfshgr':sanitize_numeric(item.get('stfshgr')),  
                            'year':sanitize_numeric(item.get('year')) 
                        }
                    )

                    StateFuelTypeGeneration.objects.update_or_create(
                        fipsst=State.objects.get(fipsst=item.get('fipsst')),
                        defaults={ 
                            'stgenacl':sanitize_numeric(item.get('stgenacl')),
                            'stgenaol':sanitize_numeric(item.get('stgenaol')),
                            'stgenaso':sanitize_numeric(item.get('stgenaso')),
                            'stgenagt':sanitize_numeric(item.get('stgenagt')),
                            'stgenaof':sanitize_numeric(item.get('stgenaof')),
                            'stgenaop':sanitize_numeric(item.get('stgenaop')),
                            'stgenatn':sanitize_numeric(item.get('stgenatn')),
                            'stgenatr':sanitize_numeric(item.get('stgenatr')),
                            'stgenath':sanitize_numeric(item.get('stgenath')),
                            'stgenacy':sanitize_numeric(item.get('stgenacy')),
                            'stgenacn':sanitize_numeric(item.get('stgenacn')),
                            'stgenags':sanitize_numeric(item.get('stgenags')),
                            'stgenanc':sanitize_numeric(item.get('stgenanc')),
                            'stgenahy':sanitize_numeric(item.get('stgenahy')),
                            'stgenabm':sanitize_numeric(item.get('stgenabm')),
                            'stgenawi':sanitize_numeric(item.get('stgenawi')),
                            'year':sanitize_numeric(item.get('year'))
                        }
                    )

                    StateNonBaseloadEmissionRate.objects.update_or_create(
                        fipsst=State.objects.get(fipsst=item.get('fipsst')),
                        defaults={  
                            'stnbnox':sanitize_numeric(item.get('stnbnox')),
                            'stnbnxo':sanitize_numeric(item.get('stnbnxo')),
                            'stnbso2':sanitize_numeric(item.get('stnbso2')),
                            'stnbco2':sanitize_numeric(item.get('stnbco2')),
                            'stnbch4':sanitize_numeric(item.get('stnbch4')),
                            'stnbn2o':sanitize_numeric(item.get('stnbn2o')),
                            'stnbc2e':sanitize_numeric(item.get('stnbc2e')),
                            'stnbhg':sanitize_numeric(item.get('stnbhg')),
                            'stnbgncl':sanitize_numeric(item.get('stnbgncl')),
                            'stnbgnol':sanitize_numeric(item.get('stnbgnol')),
                            'stnbgngs':sanitize_numeric(item.get('stnbgngs')),
                            'stnbgnnc':sanitize_numeric(item.get('stnbgnnc')),
                            'stnbgnhy':sanitize_numeric(item.get('stnbgnhy')),
                            'stnbgnbm':sanitize_numeric(item.get('stnbgnbm')),
                            'stnbgnwi':sanitize_numeric(item.get('stnbgnwi')),
                            'stnbgnso':sanitize_numeric(item.get('stnbgnso')),
                            'stnbgngt':sanitize_numeric(item.get('stnbgngt')),
                            'stnbgnof':sanitize_numeric(item.get('stnbgnof')),
                            'stnbgnop':sanitize_numeric(item.get('stnbgnop')),
                            'stnbclpr':sanitize_numeric(item.get('stnbclpr')),
                            'stnbolpr':sanitize_numeric(item.get('stnbolpr')),
                            'stnbgspr':sanitize_numeric(item.get('stnbgspr')),
                            'stnbncpr':sanitize_numeric(item.get('stnbncpr')),
                            'stnbhypr':sanitize_numeric(item.get('stnbhypr')),
                            'stnbbmpr':sanitize_numeric(item.get('stnbbmpr')),
                            'stnbwipr':sanitize_numeric(item.get('stnbwipr')),
                            'stnbsopr':sanitize_numeric(item.get('stnbsopr')),
                            'stnbgtpr':sanitize_numeric(item.get('stnbgtpr')),
                            'stnbofpr':sanitize_numeric(item.get('stnbofpr')),
                            'stnboppr':sanitize_numeric(item.get('stnboppr')),
                            'year':sanitize_numeric(item.get('year')),
                        }
                    )

                return {"success": True, "message": "Data successfully inserted/updated in the State table."}
            else:
                logger.error(f"R API returned an error: {data.get('error')}")
                return {"error": f"R API returned an error: {data.get('error')}"}
        else:
            logger.error(f"Failed to connect to R API. Status: {response.status_code}")
            return {"error": f"Failed to connect to R API with status code {response.status_code}"}
    except Exception as e:
        logger.error(f"Error while processing R API data: {e}", exc_info=True)
        return {"error": str(e)}
