from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

from address import serializers
from address.permissions import IsAdminOrReadOnly
from core import models


class BaseAddressAttrViewSet(viewsets.ModelViewSet):
    '''Base ViewSet for address attributes'''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]


class CountryViewSet(BaseAddressAttrViewSet):
    serializer_class = serializers.CountrySerializer
    queryset = models.Country.objects.all()


class CountyViewSet(BaseAddressAttrViewSet):
    serializer_class = serializers.CountySerializer
    queryset = models.County.objects.all()


class CityViewSet(BaseAddressAttrViewSet):
    serializer_class = serializers.CitySerializer
    queryset = (models.City.objects
                .select_related('county__country', 'county')
                .all())


class AddressViewSet(BaseAddressAttrViewSet):
    serializer_class = serializers.AddressSerializer
    queryset = (models.Address.objects
                .select_related('city__county__country', 'city__county', 'city')
                .all())
