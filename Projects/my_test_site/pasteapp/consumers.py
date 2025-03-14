import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)

class PasteConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("trying connecting")
        self.room_group_name = 'paste_sync'
        logger.info("Connecting to paste_sync group for channel %s", self.channel_name)
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        logger.info("WebSocket accepted for channel %s", self.channel_name)

    async def disconnect(self, close_code):
        logger.info("Disconnecting channel %s with code %s", self.channel_name, close_code)
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        logger.info("Received data from %s: %s", self.channel_name, text_data)
        data = json.loads(text_data)
        message = data.get("message", "")
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'paste_message',
                'message': message,
                'name': data.get("name", "Anonymous"),
            }
        )

    async def paste_message(self, event):
        message = event['message']
        logger.info("Broadcasting message to %s: %s", self.channel_name, message)
        await self.send(text_data=json.dumps({'message': message}))
