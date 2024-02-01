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
