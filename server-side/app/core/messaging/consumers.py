from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from core.messaging._Message import Message
from core.messaging.serializer import MessageSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = None  # Initialize room_group_name to prevent AttributeError

    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
            print("WebSocket connection rejected: Anonymous user")
        else:
            self.room_group_name = f'user_{self.user.id}'
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.channel_layer.group_add('broadcast', self.channel_name)
            print(f"WebSocket connection accepted for user: {self.user}")
            await self.accept()

    async def disconnect(self, close_code):
        if self.room_group_name:  # Ensure it exists before trying to discard
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.channel_layer.group_discard('broadcast', self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get('message_type')
            content = data.get('content')
            receiver_ids = data.get('receivers', [])

            if not content:
                await self.send(json.dumps({"error": "Message content cannot be empty."}))
                return

            message = await self.create_message(
                sender=self.user,
                receiver_ids=receiver_ids,
                message_type=message_type,
                content=content
            )
            serializer_data = await self.serialize_message(message)

            if message_type == 'broadcast':
                await self.channel_layer.group_send(
                    'broadcast',
                    {'type': 'chat_message', 'message': serializer_data}
                )
            else:
                for receiver_id in receiver_ids:
                    receiver_group_name = f'user_{receiver_id}'
                    await self.channel_layer.group_send(
                        receiver_group_name,
                        {'type': 'chat_message', 'message': serializer_data}
                    )
            await self.send(json.dumps({"success": "Message sent successfully."}))
        except json.JSONDecodeError:
            await self.send(json.dumps({"error": "Invalid JSON payload."}))
        except Exception as e:
            print(f"Error processing WebSocket message: {e}")
            await self.send(json.dumps({"error": "Internal server error."}))

    @sync_to_async
    def mark_messages_as_seen(self, message_ids):
        messages = Message.objects.filter(id__in=message_ids)
        for message in messages:
            message.is_seen.add(self.user)
        print(f"Marked messages {message_ids} as seen for user {self.user}.")

    async def chat_message(self, event):
        message = event['message']
        await self.send(json.dumps({'message': message}))

    @sync_to_async
    def create_message(self, sender, receiver_ids, message_type, content):
        message = Message.objects.create(sender=sender, message_type=message_type, content=content)
        receivers = User.objects.filter(id__in=receiver_ids)
        message.receivers.set(receivers)
        return message

    @sync_to_async
    def serialize_message(self, message):
        serializer = MessageSerializer(message, context={"user": self.scope.get("user")})
        return serializer.data
