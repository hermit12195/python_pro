import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer

from chats.ws.constants import ADMIN_GROUP_NAME, STAFF_GROUP_NAME
from chats.ws.utils import get_email


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user=self.scope["user"]
        if not user.is_authenticated:
            await self.close()
            return
        if user.is_superuser:
            await  self.channel_layer.group_add(ADMIN_GROUP_NAME, self.channel_name)
        else:
            await  self.channel_layer.group_add(STAFF_GROUP_NAME, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        print("disconnected")
        user = self.scope["user"]
        if user.is_superuser:
            await  self.channel_layer.group_discard(ADMIN_GROUP_NAME, self.channel_name)
        await  self.channel_layer.group_discard(STAFF_GROUP_NAME, self.channel_name)

    async def receive_json(self, text_data=None, bytes_data=None):
        username = self.scope['user']
        email = await get_email(username)
        await self.send_json({"response": email})
        channel_layer = get_channel_layer()
        if username.is_superuser:
            await channel_layer.group_send(ADMIN_GROUP_NAME, {"type": "chat_message", "message": "test"})
        await channel_layer.group_send(STAFF_GROUP_NAME, {"type": "chat_message", "message": "test"})

    async def send_json(self, content, close=False):
        print(f"Content: {content}")
        await self.send(json.dumps(content))

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"tweet": message}))

    async def group_message(self, event):
        print(f"Received group message: {event['group_message']}")
        message=event["group_message"]
        await self.send(text_data=json.dumps({"message": message}))
