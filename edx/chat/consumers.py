from json import loads, dumps
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = f'chat_{self.id}'
        # join the group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        # Accept connection
        await self.accept()

    async def disconnect(self, code):
        #  leave the group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        """ Receive message from Web-socket """

        now = timezone.now()
        text_data_json = loads(text_data)
        message = text_data_json.get('message')
        # send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'user': self.user.username,
                'datetime': now.isoformat(),
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        # Send message to web socket
        await self.send(text_data=dumps(event))
