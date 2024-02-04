from rest_framework import serializers

from core import models


class CitySerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField()

    class Meta:
        model = models.City
        fields = ['id', 'country', 'county', 'name']
        read_only_fields = ['id', 'country']

    def get_country(self, obj):
        return obj.county.country.id


class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.County
        fields = ['id', 'country', 'name']
        read_only_fields = ['id']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Country
        fields = ['id', 'name']
        read_only_fields = ['id']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = '__all__'
        read_only_fields = ['id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['country'] = instance.city.county.country.id
        representation['county'] = instance.city.county.id
        return representation
