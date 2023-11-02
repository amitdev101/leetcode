import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass  # Add disconnect handling if needed

    async def receive(self, text_data):
        response = "server recieved your message : " + text_data
        await self.send(text_data=response)
