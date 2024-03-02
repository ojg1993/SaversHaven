from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication

from address.permissions import IsAdminOrReadOnly
from core import models
from product import serializers
from product.pagination import ProductPagination
from product.permissions import IsSellerOrAdminElseReadOnly


class CategoryListViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin,
                          mixins.CreateModelMixin):
    '''Category serializer for list & create showing all categories from the root'''
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = models.Category.objects.root_nodes()


class CategoryDetailViewSet(viewsets.GenericViewSet,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin):
    '''Category Detail serializer for retrieve, update & delete'''
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = models.Category.objects.all()


class ProductListViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin):
    '''
    Processing product list or create a product
    It also takes images as a list of dictionary form,
    and process the image in serializer's custom methods
    '''
    serializer_class = serializers.ProductSerializer
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'is_sold']
    queryset = (models.Product.objects
                .select_related('seller', 'category')
                .prefetch_related('images')
                .all().order_by('-created_at')
                )
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]


class ProductDetailViewSet(viewsets.GenericViewSet,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin):
    '''
    Processing a single product retrieve, update & delete.
    image related update is handled in serializer's custom method
    '''
    serializer_class = serializers.ProductDetailSerializer
    queryset = (models.Product.objects
                .select_related('seller', 'category')
                .prefetch_related('images')
                .all()
                )
    permission_classes = [IsSellerOrAdminElseReadOnly]
    authentication_classes = [JWTAuthentication]


class FavoriteAPIView(generics.GenericAPIView,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin):
    serializer_class = serializers.FavoriteSerializer
    queryset = (models.Favorite.objects
                .select_related('user, product')
                .all())
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get('id')
        data = {'product': product_id}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
            return Response({'message': 'Favorite saved'},
                            status=status.HTTP_201_CREATED)
        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        product_id = self.kwargs.get('id')
        try:
            favorite = models.Favorite.objects.get(product=product_id,
                                                   user=request.user)
            self.perform_destroy(favorite)
            return Response({'message': 'Favorite removed'},
                            status=status.HTTP_204_NO_CONTENT)
        except models.Favorite.DoesNotExist:
            raise ValidationError({'message': 'Not saved as a favorite'})
