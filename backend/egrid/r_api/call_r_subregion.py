import requests 
from egrid.models import SubrgnAnnualCombustion, Subregion, SubrgnEmissionRate, SubrgnFuelTypeEmissionRate 
import requests 
import logging

logger = logging.getLogger('egrid')

def sanitize_numeric(value):
    try:
        return float(value)  # Convert to a float or int
    except (ValueError, TypeError):
        return None  # Return None for invalid values

def call_r_subregion():
    try:
        response = requests.get("http://127.0.0.1:8001/subregion")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                subrgn_data = data.get('data', [])
                # logger.debug('subrgn_data is: ', subrgn_data)
                if not subrgn_data:
                    logger.warning("R API returned no data. Skipping database update.")
                    return {"success": False, "message": "R API returned no data."}

                for item in subrgn_data:
                    subregion, created = Subregion.objects.update_or_create(
                        subrgn=item.get('subrgn'), 
                        defaults={
                            'srname':item.get('srname'), 
                        }
                    ) 
                    
                    SubrgnAnnualCombustion.objects.update_or_create(
                        subrgn=Subregion.objects.get(subrgn=item.get('subrgn')),
                        defaults={ 
                            'srhtian':sanitize_numeric(item.get('srhtian')),
                            'srhtioz':sanitize_numeric(item.get('srhtioz')),
                            'srhtiant':sanitize_numeric(item.get('srhtiant')),
                            'srhtiozt':sanitize_numeric(item.get('srhtiozt')),
                            'srngenan':sanitize_numeric(item.get('srngenan')),
                            'srngenoz':sanitize_numeric(item.get('srngenoz')),
                            'srnoxan':sanitize_numeric(item.get('srnoxan')),
                            'srnoxoz':sanitize_numeric(item.get('srnoxoz')),
                            'srso2an':sanitize_numeric(item.get('srso2an')),
                            'srco2an':sanitize_numeric(item.get('srco2an')),
                            'srch4an':sanitize_numeric(item.get('srch4an')),
                            'srn2oan':sanitize_numeric(item.get('srn2oan')),
                            'srco2eqa':sanitize_numeric(item.get('srco2eqa')),
                            'srhgan':sanitize_numeric(item.get('srhgan')),  
                            'year':sanitize_numeric(item.get('year')),
                        }
                    )  

                    SubrgnEmissionRate.objects.update_or_create(
                        subrgn=Subregion.objects.get(subrgn=item.get('subrgn')),
                        defaults={
                            'srnoxrta':sanitize_numeric(item.get('srnoxrta')),
                            'srnoxrto':sanitize_numeric(item.get('srnoxrto')),
                            'srso2rta':sanitize_numeric(item.get('srso2rta')),
                            'srco2rta':sanitize_numeric(item.get('srco2rta')),
                            'srch4rta':sanitize_numeric(item.get('srch4rta')),
                            'srn2orta':sanitize_numeric(item.get('srn2orta')),
                            'src2erta':sanitize_numeric(item.get('src2erta')),
                            'srhgrta':sanitize_numeric(item.get('srhgrta')),
                            'srnoxra':sanitize_numeric(item.get('srnoxra')),
                            'srnoxro':sanitize_numeric(item.get('srnoxro')),
                            'srso2ra':sanitize_numeric(item.get('srso2ra')),
                            'srco2ra':sanitize_numeric(item.get('srco2ra')),
                            'srch4ra':sanitize_numeric(item.get('srch4ra')),
                            'srn2ora':sanitize_numeric(item.get('srn2ora')),
                            'src2era':sanitize_numeric(item.get('src2era')),
                            'srhgra':sanitize_numeric(item.get('srhgra')),
                            'srnoxcrt':sanitize_numeric(item.get('srnoxcrt')),
                            'srnoxcro':sanitize_numeric(item.get('srnoxcro')),
                            'srso2crt':sanitize_numeric(item.get('srso2crt')),
                            'srco2crt':sanitize_numeric(item.get('srco2crt')),
                            'srch4crt':sanitize_numeric(item.get('srch4crt')),
                            'srn2ocrt':sanitize_numeric(item.get('srn2ocrt')),
                            'src2ecrt':sanitize_numeric(item.get('src2ecrt')),
                            'srhgcrt':sanitize_numeric(item.get('srhgcrt')),
                            'year':sanitize_numeric(item.get('year'))
                        }
                    )

                    SubrgnFuelTypeEmissionRate.objects.update_or_create (
                        subrgn=Subregion.objects.get(subrgn=item.get('subrgn')),
                        defaults={
                            'sronxort':sanitize_numeric(item.get('sronxort')),
                            'srgnxort':sanitize_numeric(item.get('srgnxort')),
                            'srfsnort':sanitize_numeric(item.get('srfsnort')),
                            'srcso2rt':sanitize_numeric(item.get('srcso2rt')),
                            'sroso2rt':sanitize_numeric(item.get('sroso2rt')),
                            'srgso2rt':sanitize_numeric(item.get('srgso2rt')),
                            'srfss2rt':sanitize_numeric(item.get('srfss2rt')),
                            'srcco2rt':sanitize_numeric(item.get('srcco2rt')),
                            'sroco2rt':sanitize_numeric(item.get('sroco2rt')),
                            'srgco2rt':sanitize_numeric(item.get('srgco2rt')),
                            'srfsc2rt':sanitize_numeric(item.get('srfsc2rt')),
                            'srcch4rt':sanitize_numeric(item.get('srcch4rt')),
                            'sroch4rt':sanitize_numeric(item.get('sroch4rt')),
                            'srgch4rt':sanitize_numeric(item.get('srgch4rt')),
                            'srfch4rt':sanitize_numeric(item.get('srfch4rt')),
                            'srcn2ort':sanitize_numeric(item.get('srcn2ort')),
                            'sron2ort':sanitize_numeric(item.get('sron2ort')),
                            'srgn2ort':sanitize_numeric(item.get('srgn2ort')),
                            'srfn2ort':sanitize_numeric(item.get('srfn2ort')),
                            'srcc2ert':sanitize_numeric(item.get('srcc2ert')),
                            'sroc2ert':sanitize_numeric(item.get('sroc2ert')),
                            'srgc2ert':sanitize_numeric(item.get('srgc2ert')),
                            'srfsc2ert':sanitize_numeric(item.get('srfsc2ert')),
                            'srchgrt':sanitize_numeric(item.get('srchgrt')),
                            'srfshgrt':sanitize_numeric(item.get('srfshgrt')),
                            'srcnoxr':sanitize_numeric(item.get('srcnoxr')),
                            'sronoxr':sanitize_numeric(item.get('sronoxr')),
                            'srgnoxr':sanitize_numeric(item.get('srgnoxr')),
                            'srfsnxr':sanitize_numeric(item.get('srfsnxr')),
                            'srcnxor':sanitize_numeric(item.get('srcnxor')),
                            'sronxor':sanitize_numeric(item.get('sronxor')),
                            'srgnxor':sanitize_numeric(item.get('srgnxor')),
                            'srfsnor':sanitize_numeric(item.get('srfsnor')),
                            'srcso2r':sanitize_numeric(item.get('srcso2r')),
                            'sroso2r':sanitize_numeric(item.get('sroso2r')),
                            'srgso2r':sanitize_numeric(item.get('srgso2r')),
                            'srfss2r':sanitize_numeric(item.get('srfss2r')),
                            'srcco2r':sanitize_numeric(item.get('srcco2r')),
                            'sroco2r':sanitize_numeric(item.get('sroco2r')),
                            'srgco2r':sanitize_numeric(item.get('srgco2r')),
                            'srfsc2r':sanitize_numeric(item.get('srfsc2r')),
                            'srcch4r':sanitize_numeric(item.get('srcch4r')),
                            'sroch4r':sanitize_numeric(item.get('sroch4r')),
                            'srgch4r':sanitize_numeric(item.get('srgch4r')),
                            'srfch4r':sanitize_numeric(item.get('srfch4r')),
                            'srcn2or':sanitize_numeric(item.get('srcn2or')),
                            'sron2or':sanitize_numeric(item.get('sron2or')),
                            'srgn2or':sanitize_numeric(item.get('srgn2or')),
                            'srfn2or':sanitize_numeric(item.get('srfn2or')),
                            'srcc2er':sanitize_numeric(item.get('srcc2er')),
                            'sroc2er':sanitize_numeric(item.get('sroc2er')),
                            'srgc2er':sanitize_numeric(item.get('srgc2er')),
                            'srfsc2er':sanitize_numeric(item.get('srfsc2er')),
                            'srchgr':sanitize_numeric(item.get('srchgr')),
                            'srfshgr':sanitize_numeric(item.get('srfshgr')),
                            'year':sanitize_numeric(item.get('year'))
                        }
                    )
                    # if created:
                    #     logger.info(f"Inserted new plant: {subregion.subrgn}")
                    # else:
                    #     logger.info(f"Updated existing plant: {subregion.subrgn}")

                return {"success": True, "message": "Data successfully inserted/updated in the Subregion table."}
            else:
                logger.error(f"R API returned an error: {data.get('error')}")
                return {"error": f"R API returned an error: {data.get('error')}"}
        else:
            logger.error(f"Failed to connect to R API. Status: {response.status_code}")
            return {"error": f"Failed to connect to R API with status code {response.status_code}"}
    except Exception as e:
        logger.error(f"Error while processing R API data: {e}", exc_info=True)
        return {"error": str(e)}
