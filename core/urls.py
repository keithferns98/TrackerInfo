from django.urls import path
from core.views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Products API",
        default_version="v1",
        description="Description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="<your-gmail>@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path(
        "tracker/",
        VehicleLatestInformationAPI.as_view(),
        name="latest_information_given_deviceid",
    ),
    path(
        "tracker/details/", VehicleInformationTSAPI.as_view(), name="info_given_details"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
