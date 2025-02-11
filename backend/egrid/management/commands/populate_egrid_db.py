from django.core.management.base import BaseCommand
from egrid.r_api.call_r_subregion import call_r_subregion
from egrid.r_api.call_r_plant import call_r_plant  # Import the function(s) you need
from egrid.r_api.call_r_balancing_auth import populate_balancing_auth_data
from egrid.r_api.call_r_generator import populate_generator_data 
from egrid.r_api.call_r_nerc import call_r_nerc
from egrid.r_api.call_r_state import call_r_state

# from egrid.logic.queries.plant_queries import create_or_update_plant
import logging

logger = logging.getLogger('egrid')

class Command(BaseCommand):
    help = "Populate the PostgreSQL database using functions from R API"

    def add_arguments(self, parser):
        parser.add_argument('--table_name', type=str, help="The name of the table to populate", default=None)

    def handle(self, *args, **options):
        table_name = options['table_name']
        logger.info(f"Populating the {table_name} table...")
    
        try:
           match table_name:
                case 'plant':
                   call_r_plant() # Fetch plant data from the R API
            
                case 'balancing_authority':
                    populate_balancing_auth_data()  

                case 'generator': 
                    populate_generator_data()

                case 'nerc':
                    call_r_nerc() 

                case 'state':
                    call_r_state()

                case 'subregion':
                    call_r_subregion() 
                case _:
                   # call all of them
                    call_r_state()
                    # populate_balancing_auth_data()
                    # populate_generator_data()
                    # call_r_nerc()

        except Exception as e:
            logger.error(f"Error while populating the {table_name} table: {e}", exc_info=True)
            return {"error": str(e)}