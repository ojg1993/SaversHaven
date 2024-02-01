from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

from address import serializers
from address.permissions import IsAdminOrReadOnly
from core import models


class CountryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CountrySerializer
    queryset = models.Country.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]