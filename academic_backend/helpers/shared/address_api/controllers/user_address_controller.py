from dataclasses import dataclass

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
)
from rest_framework.views import APIView, Response

from academic_backend.helpers.shared.address_api.serializers.user_address_serializer import (
    CitySerializer,
    CountrySerializer,
    UfSerializer,
)
from academic_backend.helpers.shared.address_api.services.address_service import AddressService

country_param = openapi.Parameter(
    'country',
    openapi.IN_QUERY,
    description='country described in pt-br',
    type=openapi.TYPE_STRING,
)
uf_param = openapi.Parameter(
    'uf', openapi.IN_QUERY, description='uf or district', type=openapi.TYPE_STRING
)
postalcode_param = openapi.Parameter(
    'postalcode',
    openapi.IN_QUERY,
    description='postalcode from location',
    type=openapi.TYPE_STRING,
)
postalcode_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'country': openapi.Schema(type=openapi.TYPE_STRING),
        'uf': openapi.Schema(type=openapi.TYPE_STRING),
        'city': openapi.Schema(type=openapi.TYPE_STRING),
    },
)


@dataclass()
class CountryAPIView(APIView):
    @swagger_auto_schema(
        responses={
            200: CountrySerializer,
            400: 'Bad Request',
        },
        operation_summary='Extract and show country list',
    )
    def get(self, request):
        countries = AddressService().list_all_countries()
        uk_region = AddressService().split_uk_region()
        countries.extend(uk_region)
        if countries:
            serializer = CountrySerializer(countries, many=True).data
            return Response(serializer, status=HTTP_200_OK)
        return Response(status=HTTP_404_NOT_FOUND)


@dataclass()
class UfAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[country_param],
        responses={
            200: UfSerializer,
            400: 'Bad Request',
            404: 'Country not provided or UF not found to country provided',
        },
        operation_summary='Extract and show ufs from country list',
    )
    def get(self, request):
        country_input = request.GET.get('country')
        if not country_input:
            return Response({'message': 'country not provided'}, status=HTTP_404_NOT_FOUND)

        try:
            ufs = AddressService().list_ufs_in_country(country_input)
        except:
            return Response({'message': 'country not found'}, status=HTTP_404_NOT_FOUND)

        if ufs:
            serializer = [UfSerializer(uf, many=True).data for uf in ufs]
            return Response(serializer, status=HTTP_200_OK)
        return Response(
            {'message': 'uf not found to country provided'}, status=HTTP_404_NOT_FOUND
        )


@dataclass()
class CityAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[country_param, uf_param],
        responses={
            200: CitySerializer,
            400: 'Bad Request',
            404: 'Missing UF or not country OR cities not found to uf and country provided',
        },
        operation_summary='Extract and cities from uf and country list',
    )
    def get(self, request):
        country_input = request.GET.get('country')
        uf_input = request.GET.get('uf')
        if not country_input or not uf_input:
            return Response(
                {'message': 'missing uf or country'}, status=HTTP_404_NOT_FOUND
            )
        try:
            uf_obj = AddressService().get_uf_by_name(uf_input, country_input)
        except:
            return Response({'message': 'country not found'}, status=HTTP_404_NOT_FOUND)

        if uf_obj:
            cities = AddressService().list_cities_in_uf(uf_obj[0]['geonameId'])
            serializer = CitySerializer(cities, many=True).data
            return Response(serializer, status=HTTP_200_OK)
        return Response(
            {'message': 'cities not found to uf and country provided'},
            status=HTTP_404_NOT_FOUND,
        )


@dataclass()
class PostalCodeAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[postalcode_param],
        responses={
            200: postalcode_schema,
            400: 'Bad Request',
            404: 'Postal code not provided or not found',
        },
        operation_summary='Search Location from postalcode',
    )
    def get(self, request):
        postalcode_input = request.GET.get('postalcode')
        if not postalcode_input:
            return Response(
                {'message': 'postalcode not provided'}, status=HTTP_404_NOT_FOUND
            )
        address = AddressService().list_address_by_postalcode(postalcode_input)
        if address:
            return Response(address, status=HTTP_200_OK)
        return Response({'message': 'postalcode not found'}, status=HTTP_404_NOT_FOUND)
