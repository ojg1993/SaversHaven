from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from core import models


class CategorySerializer(serializers.ModelSerializer):
    '''Tree Category serializer'''

    children = RecursiveField(many=True, read_only=True)

    class Meta:
        model = models.Category
        fields = ['id',
                  'name',
                  'parent',
                  'children'
                  ]
        read_only_fields = ['id', 'children']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ['image']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.FileField(
            max_length=1_000_000,
            allow_empty_file=False,
            use_url=False
        ),
        write_only=True)

    class Meta:
        model = models.Product
        fields = ['id',
                  'seller',
                  'category',
                  'title',
                  'price',
                  'description',
                  'images',
                  'uploaded_images',
                  'is_sold',
                  'bookmark_cnt',
                  'created_at',
                  'modified_at'
                  ]
        read_only_fields = ['id', 'seller', 'bookmark_cnt', 'is_sold']

    def create(self, validated_data):
        '''
        Creating a product
        - Passing current auth user to seller field and creating a new product.
        - Getting uploaded_images from validated_data and creating product images
        '''

        validated_data['seller'] = self.context['request'].user
        images = validated_data.pop('uploaded_images')
        product = models.Product.objects.create(**validated_data)
        for img in images:
            models.ProductImage.objects.create(product=product, image=img)
        return product


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Favorite
        fields = ('product', 'user')
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        product = validated_data['product']
        try:
            favorite = models.Favorite.objects.get(user=user, product=product)
            raise serializers.ValidationError(
                {'message': 'Already saved as a favorite'})
        except models.Favorite.DoesNotExist:
            favorite = models.Favorite.objects.create(user=user, product=product)
            return favorite


class ProductDetailSerializer(ProductSerializer):
    favorite = serializers.SerializerMethodField(read_only=True)

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ['description', 'hit_cnt', 'favorite']
        read_only_fields = ['id', 'seller', 'bookmark_cnt', 'hit_cnt']

    def get_favorite(self, product):
        favorite = models.Favorite.objects.filter(
            product=product,
            user=self.context['request'].user).exists()
        return favorite

    def update(self, instance, validated_data):
        images = validated_data.pop('uploaded_images', None)

        if images is not None:
            models.ProductImage.objects.filter(product=instance).delete()
            for img in images:
                models.ProductImage.objects.create(product=instance, image=img)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
