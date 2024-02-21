from datetime import datetime

from django.utils import timezone
from rest_framework import serializers

from core.models import DirectTransaction


class CustomDateTimeField(serializers.Field):
    """
    Extends Serializer field to represent & convert date & time data in a custom format.
    """
    def to_representation(self, value):
        # Converts date and time data to external representation
        return value.strftime("%Y-%m-%d-%H:%M")

    def to_internal_value(self, data):
        # Converts date and time data to internal value
        try:
            # Parse the input data into the given format
            time_obj = datetime.strptime(data, "%Y-%m-%d-%H:%M")
            # Add UTC timezone information to the parsed data
            time_obj = time_obj.replace(tzinfo=timezone.utc)
            return time_obj
        except ValueError:
            # Raise a ValidationError if the input data is in an invalid format
            raise serializers.ValidationError(
                "Invalid datetime format. Use 'YYYY-MM-DD-HH:MM'.")


class DirectTransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for DirectTransaction model.
    """
    title = serializers.CharField(
        source='chatroom.product.title', read_only=True)
    price = serializers.CharField(
        source='chatroom.product.price', read_only=True)
    time = CustomDateTimeField()

    class Meta:
        model = DirectTransaction
        fields = ['id',
                  'title',
                  'price',
                  'chatroom',
                  'time',
                  'location',
                  'location_detail',
                  'status',
                  'created_at',
                  'modified_at']
        read_only_fields = ['id',
                            'title',
                            'price',
                            'created_at',
                            'modified_at']

    def to_representation(self, instance):
        # Custom representation of DirectTransaction instance
        representation = super().to_representation(instance)
        # Custom formatting of datetime fields
        representation['created_at'] = (instance.created_at
                                        .strftime("%Y-%m-%d-%H:%M:%S"))
        representation['modified_at'] = (instance.modified_at
                                         .strftime("%Y-%m-%d-%H:%M:%S"))
        return representation
