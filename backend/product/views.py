from rest_framework import mixins, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

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

    # def get_serializer_class(self):
    #     if self.action == 'upload-image':
    #         return serializers.ProductImageSerializer
    #     else:
    #         return self.serializer_class
    #
    # @action(methods=['post'], detail=True, url_path='upload-image')
    # def upload_image(self, request, pk=None):
    #     product = self.get_object()
    #     serializer = self.get_serializer(product, data=request.data)
    #
    #     if serializer.is_valid():
    #         serializer.save(product=pk)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailViewSet(viewsets.GenericViewSet,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin):
    '''
    Processing a single product retrieve, update & delete.
    image related update is handled in serializer's custom method'
    '''
    serializer_class = serializers.ProductDetailSerializer
    queryset = models.Product.objects.all()
    permission_classes = [IsSellerOrAdminElseReadOnly]
    authentication_classes = [TokenAuthentication]
