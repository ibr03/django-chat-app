# chatapp/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try: 
            if not await self.authenticate_user():
                await self.close()
            else:
                self.room_name = self.scope['url_route']['kwargs']['room_name']
                self.room_group_name = f"chat_{self.room_name}"

                # Join room group
                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )

                await self.accept()
        except Exception as e:
            await self.close()
            # Handle and log the error
            print(f"WebSocket Connection Error: {str(e)}")

    async def authenticate_user(self):
        # Extract and validate the token from the WebSocket query string
        token_key = self.scope.get('query_string').decode().split('=')[1].strip()
        try:
            token = await database_sync_to_async(Token.objects.get)(key=token_key)
            user = token.user
            self.scope['user'] = user  # Attach the authenticated user to the scope
            return True
        except Token.DoesNotExist:
            print(f"WebSocket Authentication Error: {Token.DoesNotExist}")
            return False

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try: 
            data = json.loads(text_data)
            message = data['message']

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
        except Exception as e:
            # Handle and log the message processing error
            print(f"WebSocket Message Processing Error: {str(e)}")

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
