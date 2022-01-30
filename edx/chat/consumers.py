from json import loads, dumps
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = f'chat_{self.id}'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        # Accept connection
        self.accept()

    def disconnect(self, code):
        #  leave the group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        """ Receive message from Web-socket """

        text_data_json = loads(text_data)
        message = text_data_json.get('message')
        # send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_receive(self, event):
        # Send message to web socket
        self.send(text_data=dumps(event))
