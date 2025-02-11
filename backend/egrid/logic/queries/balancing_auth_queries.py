from egrid.models import BalancingAuthority

# This is getting it from the data model, not directly from R
def get_balancing_auth_by_name(bacode):
    """Fetch a plant by its unique ORISPL ID."""
    return BalancingAuthority.objects.filter(bacode=bacode).first()
