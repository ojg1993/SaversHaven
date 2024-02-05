from rest_framework import mixins, viewsets

from address.permissions import IsAdminOrReadOnly
from core import models
from product import serializers


class CategoryListViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    '''Category serializer for list & create showing all categories from the root'''
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = models.Category.objects.root_nodes()


class CategoryDetailViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    '''Category Detail serializer for retrieve, update & delete'''
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = models.Category.objects.all()
