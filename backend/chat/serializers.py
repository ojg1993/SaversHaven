from rest_framework import serializers

from core.models import ChatRoom, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class ChatRoomSerializer(serializers.ModelSerializer):

    # Fetch latest message dynamically
    latest_message = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True, source="messages.all")

    class Meta:
        model = ChatRoom
        fields = ('id',
                  'product',
                  'seller',
                  'buyer',
                  'latest_message',
                  'messages'
                  )

    def get_latest_message(self, obj):
        '''Get the latest message'''
        latest_msg = Message.objects.filter(room=obj).order_by('-created_at').first()
        if latest_msg:
            return latest_msg.text
        return None

    def create(self, validated_data):
        product = validated_data.get('product')
        seller = validated_data.get('seller')
        buyer = validated_data.get('buyer')
        chat = ChatRoom.objects.create(seller=seller, product=product, buyer=buyer)
        return chat
