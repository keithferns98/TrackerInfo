from django.shortcuts import render
from django.core.cache import cache
from rest_framework.views import APIView, Response
from core.models import VehicleLocation
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from rest_framework import status
from dateutil.parser import isoparse
from core.utils import filter_isodatetime_from_dict
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from geopy.geocoders import Photon


class VehicleLatestInformationAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "device_id",
                openapi.IN_QUERY,
                description="Parameter 1  Device id for instance (20984, 6888, 24809, 25029)\
                    outputs the given device location tracker information the distance_covered which area its currently in and list of alllatest records",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def get(self, request):
        geolocator = Nominatim(user_agent="meauserments", scheme="http")
        # geolocator = Photon(user_agent="measurements")
        param1 = request.GET.get("device_id")
        device_data = cache.get(str(param1))
        if device_data is None:
            return Response({"Error": f"This device_id-{param1} does not exists."})
        else:
            results = {}
            hits = []
            source_cords, destination_cords = None, None
            data_len = len(device_data)
            for idx, curr in enumerate(device_data):
                if idx == 0:
                    destination_cords = (curr["lat"], curr["long"])
                    results["destination_cords"] = destination_cords
                if idx == data_len - 1:
                    source_cords = (curr["lat"], curr["long"])
                    results["source_cords"] = source_cords
                hits.append(curr)
            distance = geodesic(source_cords, destination_cords)
            results["distance_covered"] = "{:.0f}km".format(distance.km)
            addr = geolocator.reverse(
                str(results["destination_cords"][0])
                + ","
                + str(results["destination_cords"][1]),
                timeout=10,
            ).raw
            results["location"] = {
                "region": addr["address"]["county"],
                "district": addr["address"]["state_district"],
                "state": addr["address"]["state"],
                "country": addr["address"]["country"],
            }
            results["latest_hits"] = hits
        return Response({f"device_id-{param1}": results})


class VehicleInformationTSAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "device_id",
                openapi.IN_QUERY,
                description="Parameter 1  Device id for instance (20984, 6888, 24809, 25029)\
                    outputs the given device location tracker information the distance_covered which area its currently in and list of alllatest records",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "start_dt",
                openapi.IN_QUERY,
                description="Parameter 2(Optional) start_dt for instance 2021-10-23T14:29:03.028049Z",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "end_dt",
                openapi.IN_QUERY,
                description="Parameter 3(Optional) end_dt for instance 2021-10-23T14:29:36.526919Z",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def get(self, request):
        device_id = request.GET.get("device_id")
        start_dt = request.GET.get("start_dt")
        end_dt = request.GET.get("end_dt")

        if device_id and start_dt and end_dt:
            device_data = cache.get(str(device_id))
            start_dt = isoparse(start_dt)
            end_dt = isoparse(end_dt)
            filtered_data = filter_isodatetime_from_dict(device_data, start_dt, end_dt)
            return Response(filtered_data)
        else:
            device_data = cache.get(str(device_id))
            total_data = len(device_data)
            results = {}
            for idx, curr in enumerate(device_data):
                if idx == 0:
                    destination_cords = (curr["lat"], curr["long"])
                    results["destination_cords"] = destination_cords
                if idx == total_data - 1:
                    source_cords = (curr["lat"], curr["long"])
                    results["source_cords"] = source_cords
            return Response((results, status.HTTP_200_OK))
