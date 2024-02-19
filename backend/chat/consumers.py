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
            # Remove current channel from the group
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
            message = content.get('message')
            sender = content.get('sender')
            room_id = content.get('room_id')

            # Check if both users and product data are available
            if not room_id:
                raise ValueError("requiring product, seller and buyer information.")

            # Get the chatroom with the extracted information
            room = await self.get_chat_room(room_id)

            # Get group name
            self.room_id = str(room.id)
            group_name = self.get_group_name(self.room_id)

            # Save received message to the DB
            await self.save_message(room, sender, message)

            # Send message to the group
            await self.channel_layer.group_send(group_name, {
                'type': 'chat_message',
                'message': message,
                'sender': sender
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
            sender = event['sender']

            # Send extracted data as json
            await self.send_json({'message': message, 'sender': sender})
        except Exception as e:
            await self.send_json({f'{e}: failed to send message'})

    @staticmethod
    def get_group_name(room_id):
        '''Generate a group name using the given room ID.'''

        return f"chat_room_{room_id}"

    @database_sync_to_async
    def get_chat_room(self, room_id):
        room = ChatRoom.objects.get(id=room_id)
        return room

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
