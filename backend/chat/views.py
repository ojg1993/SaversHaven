from django.db.models import Q
from django.http import Http404
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from chat.serializers import ChatRoomSerializer, MessageSerializer
from core.models import ChatRoom, Message, Product
from product.pagination import CustomPagination


class ChatRoomListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatRoomSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        '''get a list of chat rooms belonging to the current user'''
        user = self.request.user
        query = Q(seller=user) | Q(buyer=user)

        return ChatRoom.objects.filter(query).order_by('-created_at')

    def post(self, request, *args, **kwargs):
        '''create or get a chat room with the seller of the product'''
        product_id = self.request.data.get('product_id')
        product = Product.objects.get(id=product_id)
        seller = product.seller
        buyer = request.user

        try:
            chatroom = ChatRoom.objects.get(product=product, seller=seller, buyer=buyer)
            serializer = self.get_serializer(chatroom)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ChatRoom.DoesNotExist:
            data = {'product': product.id, 'seller': seller.id, 'buyer': buyer.id}
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)


class MessageListView(generics.ListAPIView):
    '''Get a list of messages belonging to the chatroom'''

    serializer_class = MessageSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        room_id = self.kwargs.get('room_id')

        if not room_id:
            content = {'detail': 'room_id required.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        queryset = Message.objects.filter(room=room_id)

        if not queryset.exists():
            raise Http404('Messages not found with the room_id')

        return queryset.order_by('-created_at')
