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
