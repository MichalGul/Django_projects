import json
from channels.generic.websocket import WebsocketConsumer
from icecream import ic
from asgiref.sync import async_to_sync # converts async call to sync call (creates new thread if needed, but waits)


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # accept connection
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = f'chat_{self.id}'
        ic(self.room_group_name)
        # join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        # accept connection
        self.accept()
    def disconnect(self, close_code):
        # leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    # recieve message from Websocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # send message to WebSocket
        # ic(message)
        # self.send(text_data=json.dumps({'message': message}))
        # send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    # receive message from room group
    #  named the same as the message type so that it gets executed every time a message with that specific type is received.
    def chat_message(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps(event))