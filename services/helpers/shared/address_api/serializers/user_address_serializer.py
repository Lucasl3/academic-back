from rest_framework import serializers


class CountrySerializer(serializers.Serializer):
    geonameId = serializers.IntegerField(required=True)
    countryName = serializers.CharField(max_length=200, required=True)


class UfSerializer(serializers.Serializer):
    geonameId = serializers.IntegerField(required=True)
    countryName = serializers.CharField(max_length=200, required=True)
    name = serializers.CharField(max_length=200, required=False)
    adminCodes1 = serializers.CharField(max_length=200, required=True)


class CitySerializer(serializers.Serializer):
    geonameId = serializers.IntegerField(required=True)
    name = serializers.CharField(max_length=200, required=True)
