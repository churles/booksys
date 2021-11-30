import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import PublicChatRoom, PublicChatRoomMessage
from django.contrib.auth.models import User
 
messages = []
@database_sync_to_async
def update_messages(username, message, room_name):
	chat_room = PublicChatRoom.objects.get(title=room_name)	
	user = User.objects.get(username=username)
	chat_messages = PublicChatRoomMessage(content=message, user=user, room=chat_room)
	chat_messages.save()

@database_sync_to_async
def chat_messages(room_name):
	chat_room = PublicChatRoom.objects.get(title=room_name)
	messages = PublicChatRoomMessage.objects.filter(room=chat_room).order_by('timestamp')
	return messages



class ChatRoomConsumer(AsyncWebsocketConsumer):

	async def connect(self):
		self.room_name = self.scope['url_route']['kwargs']['room_name']
		self.room_group_name = 'chat_%s' % self.room_name

		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)

		await self.accept()

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)

		message = text_data_json['message']
		username = text_data_json['username']

		await self.channel_layer.group_send(
			self.room_group_name,
				{
					'type':'chatroom_message',
					'message':message,
					'username':username
				}
			)
		
		await update_messages(username, message, self.room_name)

	async def chatroom_message(self, event):
		message = event['message']
		username = event['username']

		await self.send(text_data=json.dumps({
			'message':message,
			'username':username
		}))

	pass