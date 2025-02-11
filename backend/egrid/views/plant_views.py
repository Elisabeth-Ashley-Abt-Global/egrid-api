from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
# from egrid.logic.services.plant_service import call_r_plant, get_plant_data, sync_r_to_db
from egrid.logic.queries.plant_queries import filter_plants_by_state, get_plants_by_year
from rest_framework import status
from egrid.r_api.call_r_plant import call_r_plant

def r_plant_view(request):
    result = call_r_plant()
    
    # Use safe=False to handle non-dict responses
    return JsonResponse(result, safe=False)




class PlantListView(APIView):
    def get(self, request):
        """Fetch plant data dynamically from DB or R API."""
        plants = call_r_plant()
        return Response(plants, status=200)

class SyncRToDbView(APIView):
    def post(self, request):
        """Sync data from R API to the database."""
        call_r_plant()
        return Response({"message": "Data synced from R API to the database."}, status=200)


class FilterPlantsByStateView(APIView):
    def get(self, request, state_id):
        """
        Fetch plants filtered by state ID.
        """
        try: 
            plants = filter_plants_by_state(state_id)
            
            # Serialize the queryset (convert it into JSON-serializable data)
            plant_list = [
                {
                    'id': plant.id,
                    'plant_name': plant.plant_name,
                    'state': plant.fipsst,
                    'latitude': plant.lat,
                    'longitude': plant.lon
                } for plant in plants
            ]

            return Response(plant_list, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

class PlantsByYearView(APIView):
    def get(self, request, year):
        """
        Get all plants for a specific year.
        """
        try:
            # Call the query function to fetch plants by year
            plants = get_plants_by_year(year)
            
            # Serialize the queryset (convert it to JSON serializable data)
            plant_list = [
                {
                    'id': plant.id,
                    'seqplt': plant.seqplt,
                    'orispl': plant.orispl,
                    'plant_name': plant.plant_name,
                    'state': plant.fipsst,
                    'latitude': plant.lat,
                    'longitude': plant.lon,
                    'year': plant.year,
                } for plant in plants
            ]

            return Response(plant_list, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Error fetching plants for year {year}: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )