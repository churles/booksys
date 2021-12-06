from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import PublicChatRoom, PublicChatRoomMessage
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatRoomConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        room = PublicChatRoom.objects.get(title=self.room_name)
        messages = PublicChatRoomMessage.objects.filter(room=room).order_by('timestamp')
        content = {
            'command':'messages',
            'messages':self.messages_to_json(messages)
        }
        self.send_message(content)
    
    def latest_messages(self, data):
        author = User.objects.get(username=data['from'])
        rooms = PublicChatRoom.objects.filter(users=author)
        latest_message = []
        for room in rooms:
            latest = PublicChatRoomMessage.objects.filter(room=room).last()
            latest_message.append(latest)

        content = {
            'command':'latest_message',
            'messages':self.latest_messages_to_json(latest_message)
        }

        self.send_latest_message(content)


    def new_message(self, data):
        author = data['from']
        author_user = User.objects.get(username=author)
        room = PublicChatRoom.objects.get(title=self.room_name)

        message = PublicChatRoomMessage.objects.create(
            content=data['message'], 
            user=author_user, 
            room=room)

        content = {
            'command':'new_message',
            'message':self.message_to_json(message)
        }
        return self.send_chat_message(content)
    
    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'id':message.id,
            'author':message.user.username,
            'content':message.content,
            'timestamp':str(message.timestamp)
        }

    def latest_messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.latest_message_to_json(message))
        return result

    def latest_message_to_json(self, message):
        return {
            'id':message.id,
            'author':message.user.username,
            'room':message.room.title,
            'content':message.content,
            'timestamp':str(message.timestamp)
        }
    
    

    commands = {
        'fetch_messages':fetch_messages,
        'new_message':new_message,
        'latest_messages':latest_messages
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
			self.room_group_name,
			self.channel_name
		)
        
        self.accept()
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message
            }
        )

    def send_latest_message(self, message):
        self.send(text_data=json.dumps(message))

    def send_message(self, message):
        self.send(text_data=json.dumps(message))
    
    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))