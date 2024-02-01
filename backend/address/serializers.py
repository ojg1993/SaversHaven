from rest_framework import serializers

from core import models


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Country
        fields = '__all__'


class CountySerializer(serializers.ModelSerializer):
    country = serializers.CharField(source='country.name')
    class Meta:
        model = models.County
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    country = serializers.CharField(source='county.country.name')
    county = serializers.CharField(source='county.name')
    class Meta:
        model = models.City
        fields = '__all__'
