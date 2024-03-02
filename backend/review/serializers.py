from rest_framework import serializers

from core.models import DirectTransaction, Review


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
            'created_at',
        ]

    def validate(self, data):
        '''Validate transaction status'''
        transaction = data['transaction']
        try:
            transaction = DirectTransaction.objects.get(id=transaction.id)
        except DirectTransaction.DoesNotExist:
            raise serializers.ValidationError({
                'DirectTransaction': 'Invalid transaction ID.'
            })

        if transaction.status != 'complete':
            raise serializers.ValidationError({
                'status': 'Transaction must be completed to leave a review.'
            })
        if (transaction.chatroom.buyer != data['reviewer'] and
                transaction.chatroom.seller != data['reviewer']):
            raise serializers.ValidationError({
                'reviewer': 'You are not a participant in this transaction.'
            })
        return data

    def create(self, validated_data):
        try:
            Review.objects.get(
                transaction=validated_data['transaction'],
                reviewer=validated_data['reviewer'],
                receiver=validated_data['receiver'])
            raise serializers.ValidationError(
                {'message': 'Review already exists.'})
        except Review.DoesNotExist:
            review = Review.objects.create(**validated_data)
            return review
