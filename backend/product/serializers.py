from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from core import models


class CategorySerializer(serializers.ModelSerializer):
    '''Tree Category serializer'''
    children = RecursiveField(many=True, read_only=True)

    class Meta:
        model = models.Category
        fields = ['id', 'name', 'parent', 'children']
        read_only_fields = ['id', 'children']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ['id', 'product', 'image']
        read_only_fields = ['id', 'product']
        extra_kwargs = {'image': {'required': True}}


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)

    class Meta:
        model = models.Product
        fields = ['id', 'seller', 'category',
                  'title', 'price', 'description', 'images', 'is_sold',
                  'bookmark_cnt', 'created_at', 'is_sold', 'modified_at']
        read_only_fields = ['id', 'seller', 'bookmark_cnt']
        write_only_fields = ['description']

    def _create_images(self, images, product):
        '''
        Creating product's images upon creating or updating a product.
        This function iterates the 'images' having image information,
        and map product id while creating image object
        '''
        for image in images:
            image_obj = models.ProductImage.objects.create(
                product=product, **image
            )
            product.images.add(image_obj)

    def create(self, validated_data):
        '''
        Creating a product,
        while passing current authenticated user to seller field
        and calling '_create_image' method upon processing images field
        '''
        images = validated_data.pop('images', [])
        validated_data['seller'] = self.context['request'].user
        product = models.Product.objects.create(**validated_data)
        if images:
            self._create_images(images, product)
        return product


class ProductDetailSerializer(ProductSerializer):
    images = ProductImageSerializer(many=True)

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ['description', 'hit_cnt']
        read_only_fields = ['id', 'seller', 'bookmark_cnt', 'hit_cnt']

    def update(self, instance, validated_data):
        images = validated_data.pop('images', None)

        if images is not None:
            instance.images.clear()
            self._create_images(images, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
