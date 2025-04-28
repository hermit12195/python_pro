import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer

from blog.models import Post
from chats.ws.constants import GROUP_NAME
from chats.ws.utils import get_email


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user=self.scope["user"]
        if not user.is_authenticated:
            await self.close()
            return
        await  self.channel_layer.group_add(GROUP_NAME, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        print("disconnected")
        await  self.channel_layer.group_discard(GROUP_NAME, self.channel_name)

    async def receive_json(self, text_data=None, bytes_data=None):
        username = self.scope['user']
        email = await get_email(username)
        await self.send_json({"response": email})
        channel_layer = get_channel_layer()
        await channel_layer.group_send(GROUP_NAME, {"type": "chat_message", "message": "test"})

    async def send_json(self, content, close=False):
        print(f"Content: {content}")
        await self.send(json.dumps(content))

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"tweet": message}))
