# File to communicate with the R API
import requests 
from egrid.models import (
    BaFuelTypeGeneration,
    BaNonBaseloadEmissionRate,
    BaResourceMix, 
    BalancingAuthority, 
    BAAnnualCombustion, 
    BaEmissionRate, 
    BaFuelTypeEmissionRate
    )
import logging

logger = logging.getLogger('egrid')

def sanitize_numeric(value):
    try:
        return float(value)  # Convert to a float or int
    except (ValueError, TypeError):
        return None  # Return None for invalid values
 
def populate_balancing_auth_data():
    logger.debug("*populate_balancing_auth_data")
    try:
        response = requests.get("http://127.0.0.1:8001/balancingauthority")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                ba_data = data.get('data', [])
                logger.debug("*ba_data" + str(ba_data))

                for item in ba_data:
                    BalancingAuthority.objects.update_or_create(
                        bacode=item.get('bacode'),
                        defaults={
                            'baname': item.get('baname'),
                        }
                    )

                    BAAnnualCombustion.objects.update_or_create(
                        bacode=BalancingAuthority.objects.get(bacode=item.get('bacode')),
                        defaults={
                            'bahtian':sanitize_numeric(item.get('bahtian')),  # BA annual heat input (MMBtu)
                            'bahtioz':sanitize_numeric(item.get('bahtioz')),  # BA annual heat input (MMBtu)
                            'bahtiant':sanitize_numeric(item.get('bahtiant')),  
                            'bahtiozt':sanitize_numeric(item.get('bahtiozt')),
                            'bangenan':sanitize_numeric(item.get('bangenan')),
                            'bangenoz':sanitize_numeric(item.get('bangenoz')),
                            'banoxan':sanitize_numeric(item.get('banoxan')),
                            'banoxoz':sanitize_numeric(item.get('banoxoz')),
                            'baso2an':sanitize_numeric(item.get('baso2an')),
                            'baco2an':sanitize_numeric(item.get('baco2an')),
                            'bach4an':sanitize_numeric(item.get('bach4an')),
                            'ban2oan':sanitize_numeric(item.get('ban2oan')),
                            'baco2eqa':sanitize_numeric(item.get('baco2eqa')),
                            'bahgan':sanitize_numeric(item.get('bahgan')),
                            'year':item.get('year'),
                        }
                    )

                    BaEmissionRate.objects.update_or_create(
                        bacode=BalancingAuthority.objects.get(bacode=item.get('bacode')),
                        defaults={
                            'banoxrta':sanitize_numeric(item.get('banoxrta')),
                            'banoxrto':sanitize_numeric(item.get('banoxrto')),
                            'baso2rta':sanitize_numeric(item.get('baso2rta')),
                            'baco2rta':sanitize_numeric(item.get('baco2rta')),
                            'bach4rta':sanitize_numeric(item.get('bach4rta')),
                            'ban2orta':sanitize_numeric(item.get('ban2orta')), 
                            'bac2erta':sanitize_numeric(item.get('bac2erta')),
                            'bahgrta':sanitize_numeric(item.get('bahgrta')),
                            'banoxra':sanitize_numeric(item.get('banoxra')),
                            'banoxro':sanitize_numeric(item.get('banoxro')),
                            'baso2ra':sanitize_numeric(item.get('baso2ra')),
                            'baco2ra':sanitize_numeric(item.get('baco2ra')),
                            'bach4ra':sanitize_numeric(item.get('bach4ra')),
                            'ban2ora':sanitize_numeric(item.get('ban2ora')),
                            'bac2era':sanitize_numeric(item.get('bac2era')),
                            'bahgra':sanitize_numeric(item.get('bahgra')),
                            'banoxcrt':sanitize_numeric(item.get('banoxcrt')),
                            'banoxcro':sanitize_numeric(item.get('banoxcro')),
                            'baso2crt':sanitize_numeric(item.get('baso2crt')),
                            'baco2crt':sanitize_numeric(item.get('baco2crt')),
                            'bach4crt':sanitize_numeric(item.get('bach4crt')),
                            'ban2ocrt':sanitize_numeric(item.get('ban2ocrt')),
                            'bac2ecrt':sanitize_numeric(item.get('bac2ecrt')),
                            'bahgcrt':sanitize_numeric(item.get('bahgcrt')),
                            'year':item.get('year'),
                        }
                    )

                    BaFuelTypeEmissionRate.objects.update_or_create(
                        bacode=BalancingAuthority.objects.get(bacode=item.get('bacode')),
                        defaults={
                            'bacnoxrt':sanitize_numeric(item.get('bacnoxrt')),
                            'baonoxrt':sanitize_numeric(item.get('baonoxrt')),
                            'bagnoxrt':sanitize_numeric(item.get('bagnoxrt')),
                            'bafsnxrt':sanitize_numeric(item.get('bafsnxrt')),
                            'bacnxort':sanitize_numeric(item.get('bacnxort')),
                            'baonxort':sanitize_numeric(item.get('baonxort')),
                            'bagnxort':sanitize_numeric(item.get('bagnxort')),
                            'bafsnort':sanitize_numeric(item.get('bafsnort')),
                            'bacso2rt':sanitize_numeric(item.get('bacso2rt')),
                            'baoso2rt':sanitize_numeric(item.get('baoso2rt')),
                            'bagso2rt':sanitize_numeric(item.get('bagso2rt')),
                            'bafss2rt':sanitize_numeric(item.get('bafss2rt')),
                            'bacco2rt':sanitize_numeric(item.get('bacco2rt')),
                            'baoco2rt':sanitize_numeric(item.get('baoco2rt')),
                            'bagco2rt':sanitize_numeric(item.get('bagco2rt')),
                            'bafsc2rt':sanitize_numeric(item.get('bafsc2rt')),
                            'bacch4rt':sanitize_numeric(item.get('bacch4rt')),
                            'baoch4rt':sanitize_numeric(item.get('baoch4rt')),
                            'bagch4rt':sanitize_numeric(item.get('bagch4rt')),
                            'bafch4rt':sanitize_numeric(item.get('bafch4rt')),
                            'bacn2ort':sanitize_numeric(item.get('bacn2ort')),
                            'baon2ort':sanitize_numeric(item.get('baon2ort')),
                            'bagn2ort':sanitize_numeric(item.get('bagn2ort')),
                            'bafn2ort':sanitize_numeric(item.get('bafn2ort')),
                            'bacc2ert':sanitize_numeric(item.get('bacc2ert')),
                            'baoc2ert':sanitize_numeric(item.get('baoc2ert')),
                            'bagc2ert':sanitize_numeric(item.get('bagc2ert')),
                            'bafsc2er':sanitize_numeric(item.get('bafsc2er')),
                            'bachgrt':sanitize_numeric(item.get('bachgrt')),
                            'bafshgrt':sanitize_numeric(item.get('bafshgrt')),
                            'bacnoxr':sanitize_numeric(item.get('bacnoxr')),
                            'baonoxr':sanitize_numeric(item.get('baonoxr')),
                            'bagnoxr':sanitize_numeric(item.get('bagnoxr')),
                            'bafsnxr':sanitize_numeric(item.get('bafsnxr')),
                            'bacnxor':sanitize_numeric(item.get('bacnxor')),
                            'baonxor':sanitize_numeric(item.get('baonxor')),
                            'bagnxor':sanitize_numeric(item.get('bagnxor')),
                            'bafsnor':sanitize_numeric(item.get('bafsnor')),
                            'bacso2r':sanitize_numeric(item.get('bacso2r')),
                            'baoso2r':sanitize_numeric(item.get('baoso2r')),
                            'bagso2r':sanitize_numeric(item.get('bagso2r')),
                            'bafss2r':sanitize_numeric(item.get('bafss2r')),
                            'bacco2r':sanitize_numeric(item.get('bacco2r')),
                            'baoco2r':sanitize_numeric(item.get('baoco2r')),
                            'bagco2r':sanitize_numeric(item.get('bagco2r')),
                            'bafsc2r':sanitize_numeric(item.get('bafsc2r')),
                            'bacch4r':sanitize_numeric(item.get('bacch4r')),
                            'baoch4r':sanitize_numeric(item.get('baoch4r')),
                            'bagch4r':sanitize_numeric(item.get('bagch4r')),
                            'bafch4r':sanitize_numeric(item.get('bafch4r')),
                            'bacn2or':sanitize_numeric(item.get('bacn2or')),
                            'baon2or':sanitize_numeric(item.get('baon2or')),
                            'bagn2or':sanitize_numeric(item.get('bagn2or')),
                            'bafn2or':sanitize_numeric(item.get('bafn2or')),
                            'bacc2er':sanitize_numeric(item.get('bacc2er')),
                            'baoc2er':sanitize_numeric(item.get('baoc2er')),
                            'bagc2er':sanitize_numeric(item.get('bagc2er')),
                            'bafsc2er':sanitize_numeric(item.get('bafsc2er')),
                            'bachgr':sanitize_numeric(item.get('bachgr')),
                            'bafshgr':sanitize_numeric(item.get('bafshgr')),
                            'year':item.get('year')
                        }
                    )

                    BaFuelTypeGeneration.objects.update_or_create(
                        bacode=BalancingAuthority.objects.get(bacode=item.get('bacode')),
                        defaults={
                            'bagenacl':sanitize_numeric(item.get('bagenacl')),
                            'bagenaol':sanitize_numeric(item.get('bagenaol')),
                            'bagenags':sanitize_numeric(item.get('bagenags')),
                            'bagenanc':sanitize_numeric(item.get('bagenanc')),
                            'bagenahy':sanitize_numeric(item.get('bagenahy')),
                            'bagenabm':sanitize_numeric(item.get('bagenabm')),
                            'bagenawi':sanitize_numeric(item.get('bagenawi')),
                            'bagenaso':sanitize_numeric(item.get('bagenaso')),
                            'bagenagt':sanitize_numeric(item.get('bagenagt')),
                            'bagenaof':sanitize_numeric(item.get('bagenaof')),
                            'bagenaop':sanitize_numeric(item.get('bagenaop')),
                            'bagenatn':sanitize_numeric(item.get('bagenatn')),
                            'bagenatr':sanitize_numeric(item.get('bagenatr')),
                            'bagenath':sanitize_numeric(item.get('bagenath')),
                            'bagenacy':sanitize_numeric(item.get('bagenacy')),
                            'bagenacn':sanitize_numeric(item.get('bagenacn')),
                            'year':item.get('year')
                        }
                    )

                    BaFuelTypeGeneration.objects.update_or_create(
                        bacode=BalancingAuthority.objects.get(bacode=item.get('bacode')),
                        defaults={
                            'banbnox':sanitize_numeric(item.get('banbnox')),
                            'banbnxo':sanitize_numeric(item.get('banbnxo')),
                            'banbso2':sanitize_numeric(item.get('banbso2')),
                            'banbco2':sanitize_numeric(item.get('banbco2')),
                            'banbch4':sanitize_numeric(item.get('banbch4')),
                            'banbn2o':sanitize_numeric(item.get('banbn2o')),
                            'banbc2e':sanitize_numeric(item.get('banbc2e')),
                            'banbhg':sanitize_numeric(item.get('banbhg')),
                            'banbgncl':sanitize_numeric(item.get('banbgncl')),
                            'banbgnol':sanitize_numeric(item.get('banbgnol')),
                            'banbgngs':sanitize_numeric(item.get('banbgngs')),
                            'banbgnnc':sanitize_numeric(item.get('banbgnnc')),
                            'banbgnhy':sanitize_numeric(item.get('banbgnhy')),
                            'banbgnbm':sanitize_numeric(item.get('banbgnbm')),
                            'banbgnwi':sanitize_numeric(item.get('banbgnwi')),
                            'banbgnso':sanitize_numeric(item.get('banbgnso')),
                            'banbgngt':sanitize_numeric(item.get('banbgngt')),
                            'banbgnof':sanitize_numeric(item.get('banbgnof')),
                            'banbgnop':sanitize_numeric(item.get('banbgnop')),
                            'banbclpr':sanitize_numeric(item.get('banbclpr')),
                            'banbolpr':sanitize_numeric(item.get('banbolpr')),
                            'banbgspr':sanitize_numeric(item.get('banbgspr')),
                            'banbncpr':sanitize_numeric(item.get('banbncpr')),
                            'banbhypr':sanitize_numeric(item.get('banbhypr')),
                            'banbbmpr':sanitize_numeric(item.get('banbbmpr')),
                            'banbwipr':sanitize_numeric(item.get('banbwipr')),
                            'banbsopr':sanitize_numeric(item.get('banbsopr')),
                            'banbgtpr':sanitize_numeric(item.get('banbgtpr')),
                            'banbofpr':sanitize_numeric(item.get('banbofpr')),
                            'banboppr':sanitize_numeric(item.get('banboppr')),
                            'year':item.get('year')
                        }
                    )

                    BaNonBaseloadEmissionRate.objects.update_or_create(
                        bacode=BalancingAuthority.objects.get(bacode=item.get('bacode')),
                        defaults={
                        'banbnox':sanitize_numeric(item.get('banbnox')),
                        'banbnxo':sanitize_numeric(item.get('banbnxo')),
                        'banbso2':sanitize_numeric(item.get('banbso2')),
                        'banbco2':sanitize_numeric(item.get('banbco2')),
                        'banbch4':sanitize_numeric(item.get('banbch4')),
                        'banbn2o':sanitize_numeric(item.get('banbn2o')),
                        'banbc2e':sanitize_numeric(item.get('banbc2e')),
                        'banbhg':sanitize_numeric(item.get('banbhg')),
                        'banbgncl':sanitize_numeric(item.get('banbgncl')),
                        'banbgnol':sanitize_numeric(item.get('banbgnol')),
                        'banbgngs':sanitize_numeric(item.get('banbgngs')),
                        'banbgnnc':sanitize_numeric(item.get('banbgnnc')),
                        'banbgnhy':sanitize_numeric(item.get('banbgnhy')),
                        'banbgnbm':sanitize_numeric(item.get('banbgnbm')),
                        'banbgnwi':sanitize_numeric(item.get('banbgnwi')),
                        'banbgnso':sanitize_numeric(item.get('banbgnso')),
                        'banbgngt':sanitize_numeric(item.get('banbgngt')),
                        'banbgnof':sanitize_numeric(item.get('banbgnof')),
                        'banbgnop':sanitize_numeric(item.get('banbgnop')),
                        'banbclpr':sanitize_numeric(item.get('banbclpr')),
                        'banbolpr':sanitize_numeric(item.get('banbolpr')),
                        'banbgspr':sanitize_numeric(item.get('banbgspr')),
                        'banbncpr':sanitize_numeric(item.get('banbncpr')),
                        'banbhypr':sanitize_numeric(item.get('banbhypr')),
                        'banbbmpr':sanitize_numeric(item.get('banbbmpr')),
                        'banbwipr':sanitize_numeric(item.get('banbwipr')),
                        'banbsopr':sanitize_numeric(item.get('banbsopr')),
                        'banbgtpr':sanitize_numeric(item.get('banbgtpr')),
                        'banbofpr':sanitize_numeric(item.get('banbofpr')),
                        'banboppr':sanitize_numeric(item.get('banboppr')),
                        'year':item.get('year')
                        }
                    )

                    BaResourceMix.objects.update_or_create(
                        bacode=BalancingAuthority.objects.get(bacode=item.get('bacode')),
                        defaults={
                            'baclpr':sanitize_numeric(item.get('baclpr')),
                            'baolpr':sanitize_numeric(item.get('baolpr')),
                            'bagspr':sanitize_numeric(item.get('bagspr')),
                            'bancpr':sanitize_numeric(item.get('bancpr')),
                            'bahypr':sanitize_numeric(item.get('bahypr')),
                            'babmpr':sanitize_numeric(item.get('babmpr')),
                            'bawipr':sanitize_numeric(item.get('bawipr')),
                            'basopr':sanitize_numeric(item.get('basopr')),
                            'bagtpr':sanitize_numeric(item.get('bagtpr')),
                            'baofpr':sanitize_numeric(item.get('baofpr')),
                            'baoppr':sanitize_numeric(item.get('baoppr')),
                            'batnpr':sanitize_numeric(item.get('batnpr')),
                            'batrpr':sanitize_numeric(item.get('batrpr')),
                            'bathpr':sanitize_numeric(item.get('bathpr')),
                            'bacypr':sanitize_numeric(item.get('bacypr')),
                            'bacnpr':sanitize_numeric(item.get('bacnpr')),
                            'year':item.get('year')
                        }
                    )

                return {"success": True, "message": "Data successfully inserted into the Balancing Auth table."}
            else:
                return {"error": "R API returned an error: {}".format(data.get('error'))}
        else:
            return {"error": "Failed to connect to R API with status code {}".format(response.status_code)}
    except Exception as e:
        return {"error": str(e)}