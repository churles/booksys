import profile
from django.shortcuts import render, redirect
from django.http import HttpResponse
from books.models import Book
from .models import PublicChatRoom, PublicChatRoomMessage
from django.contrib.auth.decorators import login_required
from accounts.models import Profile

def index(request):
	if request.method == 'POST':
		book_id = request.POST.get('book')
		user_id = request.user.id
		book = Book.objects.get(id=book_id)		
		room_name = 'room' +str(book_id) +str(user_id)
		user = [request.user, book.owner]
		chat_room = PublicChatRoom(title=room_name, book=book)
		chat_room.save()
		chat_room.users.add(request.user)
		chat_room.users.add(book.owner)

		chat_messages = PublicChatRoomMessage(content="Hello, I would like to rent " + book.title, user=request.user, room=chat_room)
		chat_messages.save()
	return redirect('chat:room', room_name=room_name)

def book_messages(request):
	if request.method == 'GET':
		book = Book.objects.get(id=request.GET.get('book'))
		chat_room = PublicChatRoom.objects.filter(book=book, users__in=[request.user, book.owner])[0]

	return redirect('chat:room', room_name=chat_room.title)

@login_required(login_url="/accounts/login/")
def room(request, room_name):

	chat_room = PublicChatRoom.objects.get(title=room_name)
	messages = PublicChatRoomMessage.objects.filter(room=chat_room).order_by('timestamp')
	rooms = PublicChatRoom.objects.filter(users=request.user)
	profiles = Profile.objects.all()

	return render(request, 'chat/chatroom.html',{
		'room_name':room_name,
		'messages':messages,
		'rooms':rooms,
		'profiles':profiles
	})

def user_messages(request):
	chat_room = PublicChatRoom.objects.filter(users=request.user)
	room = chat_room.exclude(deleted_by=request.user)
	if not room:
		return HttpResponse('test')
	else:

		messages = PublicChatRoomMessage.objects.filter(room=room[0]).order_by('timestamp')
		profiles = Profile.objects.all()

		return render(request, 'chat/chatroom.html',{
			'room_name':room[0].title,
			'messages':messages,
			'rooms':room,
			'profiles':profiles
		})

def room_delete(request, room_id):
	room = PublicChatRoom.objects.get(id=room_id)
	room.deleted = "true"
	room.save()
	room.deleted_by.add(request.user)
	return redirect('books:list')