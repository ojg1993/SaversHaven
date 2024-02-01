from rest_framework import serializers

from core import models


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Country
        fields = '__all__'


class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.County
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = '__all__'
