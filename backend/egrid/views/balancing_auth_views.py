from django.shortcuts import render
from django.http import JsonResponse
from egrid.r_api.call_r_balancing_auth import populate_balancing_auth_data
from egrid.logic.queries.balancing_auth_queries import get_balancing_auth_by_name
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from egrid.models import BalancingAuthority
from rest_framework.response import Response

def r_ba_view(request):
    result = populate_balancing_auth_data()
    return JsonResponse(result)

class ba_list_view(APIView):
    """Fetch all balancing authorities."""
    def get(self, request, bacode):
        balancing_auths = get_balancing_auth_by_name(bacode)
        return JsonResponse(balancing_auths, safe=False)

# View to send data to R API (POST)
# def r_process_view(request):
#     input_data = request.GET.get("input_data", "Default Data")  # Example: get input from query params
#     result = send_data_to_r(input_data)
#     return JsonResponse(result)
 

class BalancingAuthorityView(APIView):
    """
    Retrieve balancing authority details by `baname` or `bacode`.
    """

    # Define Swagger parameters
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('baname', openapi.IN_QUERY, description="Filter by balancing authority name", type=openapi.TYPE_STRING),
            openapi.Parameter('bacode', openapi.IN_QUERY, description="Filter by balancing authority code", type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request):
        baname = request.GET.get('baname', None)
        bacode = request.GET.get('bacode', None)

        # Apply filtering based on received parameters
        queryset = BalancingAuthority.objects.all()
        if baname:
            queryset = queryset.filter(bacode=baname)
        if bacode:
            queryset = queryset.filter(bacode=bacode)

        # Serialize response
        data = list(queryset.values("baname", "bacode"))  # Adjust fields as needed
        return Response({"success": True, "data": data})