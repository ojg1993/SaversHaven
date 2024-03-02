from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from address import serializers
from address.permissions import IsAdminOrReadOnly
from core import models
from product.pagination import CustomPagination


class BaseAddressAttrViewSet(viewsets.ModelViewSet):
    '''Base ViewSet for address attributes'''
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = CustomPagination


class CountryViewSet(BaseAddressAttrViewSet):
    serializer_class = serializers.CountrySerializer
    queryset = models.Country.objects.all().order_by('-id')


class CountyViewSet(BaseAddressAttrViewSet):
    serializer_class = serializers.CountySerializer
    queryset = models.County.objects.all().order_by('-id')


class CityViewSet(BaseAddressAttrViewSet):
    serializer_class = serializers.CitySerializer
    queryset = (models.City.objects
                .select_related('county__country', 'county')
                .all().order_by('-id'))


class AddressViewSet(BaseAddressAttrViewSet):
    serializer_class = serializers.AddressSerializer
    permission_classes = [IsAuthenticated]
    queryset = (models.Address.objects
                .select_related('city__county__country', 'city__county', 'city')
                .all().order_by('-id'))
