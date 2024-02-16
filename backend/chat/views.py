from rest_framework import generics, status
from rest_framework.response import Response
from core.models import ChatRoom, Message, User
from chat.serializers import ChatRoomSerializer, MessageSerializer
from rest_framework.exceptions import ValidationError
from django.http import Http404
from django.db.models import Q



class ImmediateResponseException(Exception):
    '''
    Custom exception classes.
    used for immediate HTTP response when an exception is thrown
    '''
    def __init__(self, response):
        self.response = response


class ChatRoomListCreateView(generics.ListCreateAPIView):
    '''for viewing and creating chat room lists'''

    serializer_class = ChatRoomSerializer

    def get_queryset(self):
        '''Methods to define a queryset for a GET request'''

        try:
            # product = self.request.query_params.get('product', None)
            user_nickname = self.request.query_params.get('nickname', None)

            if not user_nickname:
                raise ValidationError('Nickname required.')

            # Filter the chat room that the nickname belongs to
            return ChatRoom.objects.filter(
                Q(seller__nickname=user_nickname) |
                Q(buyer__nickname=user_nickname)
            )

        except ValidationError as e:
            # On ValidationError error, return error details with 400 code
            content = {'detail': e.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # On other errors, return error details with 400 code
            content = {'detail': str(e)}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_context(self):
        # Call the super class's serializer context
        context = super(ChatRoomListCreateView, self).get_serializer_context()
        # Add the current request object to the context
        context['request'] = self.request
        return context

    def create(self, request, *args, **kwargs):
        # Serialise requested data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except ImmediateResponseException as e:
            return e.response

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        product = self.request.data.get('product')
        seller_nickname = self.request.data.get('seller_nickname')
        buyer_nickname = self.request.data.get('buyer_nickname')

        seller = User.objects.get(nickname=seller_nickname)
        buyer = User.objects.get(nickname=buyer_nickname)

        existing_chatroom = ChatRoom.objects.filter(product=product,
                                                    seller=seller,
                                                    buyer=buyer).first()

        if existing_chatroom:
            serializer = ChatRoomSerializer(existing_chatroom, context={'request': self.request})
            raise ImmediateResponseException(Response(serializer.data, status=status.HTTP_200_OK))

        serializer.save(product=product, seller=seller, buyer=buyer)


class MessageListView(generics.ListAPIView):
    '''View a list of messages'''

    serializer_class = MessageSerializer

    def get_queryset(self):
        room_id = self.kwargs.get('room_id')

        # if room_id doesn't exist return 400 code
        if not room_id:
            content = {'detail': 'room_id required.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        queryset = Message.objects.filter(room_id=room_id)

        if not queryset.exists():
            raise Http404('Messages not found with the room_id')

        return queryset