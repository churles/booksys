from django.shortcuts import render, redirect
from django.http import HttpResponse
from books.models import Book
from .models import PublicChatRoom, PublicChatRoomMessage
from django.contrib.auth.decorators import login_required

def index(request):
	if request.method == 'POST':
		book_id = request.POST.get('book')
		user_id = request.user.id
		book = Book.objects.get(id=book_id)		
		room_name = 'room' +str(book_id) +str(user_id)
		user = [request.user, book.owner]
		chat_room = PublicChatRoom(title=room_name)
		chat_room.save()
		chat_room.users.add(request.user)
		chat_room.users.add(book.owner)

		chat_messages = PublicChatRoomMessage(content="Hello, I would like to rent " + book.title, user=request.user, room=chat_room)
		chat_messages.save()
	return redirect('chat:room', room_name=room_name)

@login_required(login_url="/accounts/login/")
def room(request, room_name):

	chat_room = PublicChatRoom.objects.get(title=room_name)
	messages = PublicChatRoomMessage.objects.filter(room=chat_room).order_by('timestamp')
	rooms = PublicChatRoom.objects.filter(users=request.user)

	return render(request, 'chat/chatroom.html',{
		'room_name':room_name,
		'messages':messages,
		'rooms':rooms
	})