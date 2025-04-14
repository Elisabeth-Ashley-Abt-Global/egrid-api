from django.core.management.base import BaseCommand
from egrid.r_api.call_r_subregion import populate_subregion_data
from egrid.r_api.call_r_plant import populate_plant_data  
from egrid.r_api.call_r_balancing_auth import populate_balancing_auth_data
from egrid.r_api.call_r_generator import populate_generator_data 
from egrid.r_api.call_r_nerc import populate_nerc_data
from egrid.r_api.call_r_state import populate_state_data 
from egrid.r_api.call_r_us import populate_us_data
from egrid.r_api.call_r_unit import populate_unit_data
from sqlalchemy import create_engine, text 
from urllib.parse import quote_plus
from django.conf import settings
# from egrid.logic.queries.plant_queries import create_or_update_plant
import logging
schema = 'egrid-dev'
options = quote_plus(f'-c search_path={schema}')

logger = logging.getLogger('egrid')
api_url = 'http://127.0.0.1:8001/'

engine = create_engine(
    f"postgresql://{settings.DATABASES['default']['USER']}:{settings.DATABASES['default']['PASSWORD']}@"
    f"{settings.DATABASES['default']['HOST']}:{settings.DATABASES['default']['PORT']}/"
    f"{settings.DATABASES['default']['NAME']}?options={options}"
)   

class Command(BaseCommand):
    help = "Populate the PostgreSQL database using functions from R API"

    def add_arguments(self, parser):
        parser.add_argument('--table_name', type=str, help="The name of the table to populate", default=None)
        parser.add_argument('--year', type=int, help="The year to populate", default=None)

    def handle(self, *args, **options):
        table_name = options['table_name']
        year = options['year']
        logger.info(f"Populating the {table_name} table...")
    
        try:
           match table_name:
                case 'plant':
                   populate_plant_data(engine, api_url, year) # Fetch plant data from the R API
            
                case 'balancing_authority':
                    populate_balancing_auth_data(engine, api_url)  

                case 'generator': 
                    populate_generator_data(engine, api_url) # Fetch generator data from the R API

                case 'nerc':
                    populate_nerc_data(engine, api_url) 

                case 'state':
                    populate_state_data(engine, api_url, year)

                case 'subregion':
                    populate_subregion_data(engine, api_url, year) 

                case 'us':
                   populate_us_data(engine, api_url, year)
                    
                case 'unit': 
                   populate_unit_data(engine, api_url, year)  
                # case _:
                #    # call all of them
                #     call_r_unit()
                    # populate_balancing_auth_data()
                    # populate_generator_data()
                    # call_r_nerc()

        except Exception as e:
            logger.error(f"Error while populating the {table_name} table: {e}", exc_info=True)
            return {"error": str(e)}