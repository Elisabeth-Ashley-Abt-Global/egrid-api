from egrid.models import Plant

def get_all_plants():
    """Fetch all plants from the database."""
    return Plant.objects.all()

def get_plant_by_orispl(orispl):
    """Fetch a plant by its unique ORISPL ID."""
    return Plant.objects.filter(orispl=orispl).first()

def create_or_update_plant(data):
    """Create or update a plant using a dictionary of data and a year."""
    return Plant.objects.update_or_create(
        seqplt=data.get('seqplt'),
        defaults={
            'orispl': data.get('orispl'),
            'pstatabb': data.get('pstatabb'),
            'fipsst': data.get('fipsst'),
            'plant_name': data.get('plant_name'),
            'oprcode': data.get('oprcode'),
            'utlsrvid': data.get('utlsrvid'),
            'sector_id': data.get('sector_id'),
            'bacode': data.get('bacode'),
            'nerc': data.get('nerc'),
            'fipscnty': data.get('fipscnty'),
            'lat': data.get('lat'),
            'lon': data.get('lon'),
            'numunt': data.get('numunt'),
            'numgen': data.get('numgen'),
            'plprmfl': data.get('plprmfl'),
            'plfuelct': data.get('plfuelct'),
            'coalflagind': data.get('coalflagind'),
            'subrgn_id': data.get('subrgn_id'),
            'year': data.get('year'),   
        }
    )


def filter_plants_by_state(state_id):
    """Fetch plants filtered by state."""
    return Plant.objects.filter(fipsst=state_id)

def delete_plant(orispl):
    """Delete a plant by its ORISPL ID."""
    return Plant.objects.filter(orispl=orispl).delete()

def get_plants_by_year(year): 
    return Plant.objects.filter(year=year)
