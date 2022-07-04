import json
from channels.generic.websocket import WebsocketConsumer
from icecream import ic

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # accept connection
        self.accept()
    def disconnect(self, close_code):
        pass
    
    # recieve message from Websocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # send message to WebSocket
        ic(message)
        self.send(text_data=json.dumps({'message': message}))