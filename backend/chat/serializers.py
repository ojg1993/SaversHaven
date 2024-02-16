from rest_framework import serializers
from core.models import ChatRoom, Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

class ChatRoomSerializer(serializers.ModelSerializer):

    # Fetch latest message dynamically
    latest_message = serializers.SerializerMethodField()
    # Fetch opponent's nickname dynamically
    opponent_nickname = serializers.SerializerMethodField()

    seller_nickname = serializers.SerializerMethodField()
    buyer_nickname = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True, source="messages.all")

    class Meta:
        model = ChatRoom
        fields = ('id',
                  'seller_nickname',
                  'buyer_nickname',
                  'latest_message',
                  'opponent_nickname',
                  'messages'
                  )

    def get_latest_message(self, obj):
        '''Get the latest message'''
        latest_msg = Message.objects.filter(room=obj).order_by('-created_at').first()
        if latest_msg:
            return latest_msg.text
        return None

    def get_opponent_nickname(self, obj):
        '''Get the opponent's nickname'''
        request_user_nickname = self.context['request'].query_params.get('nickname', None)
        # if request user is seller return buyer's nickname
        if request_user_nickname == obj.seller.nickname:
            return obj.buyer.nickname
        else:  # or return seller's nickname
            return obj.seller.nickname

    def get_seller_nickname(self, obj):
        '''Get the seller nickname'''
        return obj.seller.nickname

    def get_buyer_nickname(self, obj):
        '''Get the buyer nickname'''
        return obj.buyer.nickname