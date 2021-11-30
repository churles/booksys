from django.shortcuts import render, redirect
from django.http import HttpResponse
from books.models import Book
from .models import PublicChatRoom, PublicChatRoomMessage

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

def room(request, room_name):
	return render(request, 'chat/chatroom.html',{
		'room_name':room_name
	})