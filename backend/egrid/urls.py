from django.urls import path, re_path
# from .views.balancing_auth_views import r_hello_view, r_ba_view
from .views.plant_views import ( 
    FilterPlantsByStateView, 
    PlantsByYearView,
    r_plant_view
)
from .views.balancing_auth_views import (
    r_ba_view,
    ba_list_view,
    BalancingAuthorityView  
)

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi 
 
schema_view = get_schema_view(
    openapi.Info(
        title="eGrid API",
        default_version='v1',
        description="API documentation for eGrid API",
        terms_of_service="placeholder",
        contact=openapi.Contact(email="placeholderusername"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # path('r-hello/', r_hello_view, name='r_hello'),
    # path('r-process/', r_process_view, name='r_process'),
    path('r-plant/', r_plant_view, name='r_plant'), 
    path('r-ba/', r_ba_view, name='r_ba_view'),
    # path('plant/<str:plant_id>/', r_plant_view, name='r_plant'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('plants/', plant_views.PlantListView.as_view(), name='plant_list'),
    path('plants/state/<str:state_id>/', FilterPlantsByStateView.as_view(), name='filter_plants_by_state'),
    path('plants/year/<int:year>/', PlantsByYearView.as_view(), name='plants_by_year'),
    path('balancing-authority/', BalancingAuthorityView.as_view(), name='balancing_authority'),

]
