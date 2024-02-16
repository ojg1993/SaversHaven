from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from core.models import ChatRoom, Message


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        '''
        Called when a client tries to connect to the websocket.
        It extracts the room ID from the URL path, verifies if the room exists,
          and adds the current channel to that group.
        If the connection is successful, it accepts the connection to notify the client.
        '''

        try:
            # Extract room_id from URL path
            self.room_id = self.scope['url_route']['kwargs']['room_id']

            # Check if the room exists
            if not await self.check_room_exists(self.room_id):
                raise ValueError('Chatroom does not exist')

            # Get group_name with the given room_id
            group_name = self.get_group_name(self.room_id)

            # Add current channel to the group
            await self.channel_layer.group_add(group_name,
                                               self.channel_name)
            await self.accept()  # Accept WebSocket connection

        # if error raised return error message, and close the connection
        except ValueError as e:
            await self.send_json({'error': str(e)})
            await self.close()

    async def disconnect(self, close_code):
        '''
        Called when the client terminates the websocket connection.
        Removes the current channel from its group.
        '''

        try:
            # Get group name with room_id
            group_name = self.get_group_name(self.room_id)
            # Remove current channel from the groupb
            await self.channel_layer.group_discard(group_name, self.channel_name)

        except Exception as e:
            await self.send_json({'error': str(e)})

    async def receive_json(self, content):
        '''
        Called when a JSON message is received from a client.
        It stores the received message in the database,
         and sends the message to all clients in the same group.
        '''

        try:
            # Extract information from the received json
            message = content['message']
            sender_nickname = content['sender_nickname']
            product = content.get('product')
            seller_nickname = content.get('seller_nickname')
            buyer_nickname = content.get('buyer_nickname')

            # Check if both users and product data are available
            if not seller_nickname or not buyer_nickname or not product:
                raise ValueError("requiring product, seller's and buyer's information.")

            # Get or create a chatroom with the extracted information
            room = await self.get_or_create_room(product, seller_nickname, buyer_nickname)

            # Update room_id data type
            self.room_id = str(room.id)

            # Get group name
            group_name = self.get_group_name(self.room_id)

            # Save received message to the DB
            await self.save_message(room, sender_nickname, message)

            # Send message to the group
            await self.channel_layer.group_send(group_name, {
                'type': 'chat_message',
                'message': message,
                'sender_nickname': sender_nickname  # Add sender info
            })

        except ValueError as e:
            await self.send_json({'error': str(e)})

    async def chat_message(self, event):
        '''
        Called when a message is received from another client in the group.
        Sends the received message to the current channel(client).
        '''

        try:
            # Extract message and sender info from the event
            message = event['message']
            sender_nickname = event['sender_nickname']

            # Send extracted data as json
            await self.send_json({'message': message, 'sender_nickname': sender_nickname})
        except Exception as e:
            await self.send_json({f'{e}: failed to send message'})

    @staticmethod
    def get_group_name(room_id):
        '''Generate a group name using the given room ID.'''

        return f"chat_room_{room_id}"

    @database_sync_to_async
    def get_or_create_room(self, product, seller_nickname, buyer_nickname):
        '''
        Gets a chat room using the given email,
         or creates one if it doesn't exist.
        '''

        try:
            # Get or create a chatroom with the given data
            room, created = ChatRoom.objects.get_or_create(
                product=product,
                seller__nickname=seller_nickname,
                buyer__nickname=buyer_nickname
            )
            if created:
                return created
            else:
                return room

        except Exception as e:
            raise ValueError(f"failed to get or create a chatroom: {e}") from e

    @database_sync_to_async
    def save_message(self, room, sender_nickname, message):
        '''
        Create and save a new message with the given information
        '''

        # Check if sender and text were provided
        if not room or not sender_nickname or not message:
            raise ValueError("room, sender_nickname and message are required.")

        # Create a message and save it in DB
        Message.objects.create(room=room, sender=sender_nickname, text=message)

    @database_sync_to_async
    def check_room_exists(self, room_id):
        '''Checks if a chat room exists with the given ID.'''
        return ChatRoom.objects.filter(id=room_id).exists()
