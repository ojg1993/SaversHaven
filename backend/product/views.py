from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from address.permissions import IsAdminOrReadOnly
from core import models
from product import serializers
from product.permissions import IsSellerOrAdminElseReadOnly


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


class ProductListViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    '''
    Processing product list or create a product
    It also takes images as a list of dictionary form,
    and process the image in serializer's custom methods
    '''
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]


class ProductDetailViewSet(viewsets.GenericViewSet,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin):
    '''
    Processing a single product retrieve, update & delete.
    image related update is handled in serializer's custom method
    '''
    serializer_class = serializers.ProductDetailSerializer
    queryset = models.Product.objects.all()
    permission_classes = [IsSellerOrAdminElseReadOnly]
    authentication_classes = [TokenAuthentication]
