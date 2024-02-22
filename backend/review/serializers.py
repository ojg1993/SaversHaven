from rest_framework import serializers

from core.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    '''
    Serializer for Review model
    '''

    product_title = serializers.CharField(
        source='transaction.chatroom.product.title',
        read_only=True
    )

    class Meta:
        model = Review
        fields = [
            'id',
            'transaction',
            'reviewer',
            'receiver',
            'product_title',
            'review',
            'rating',
            'created_at'
        ]
        read_only_fields = [
            'id',
            'transaction',
            'reviewer',
            'receiver',
            'created_at',
        ]
