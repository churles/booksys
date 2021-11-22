from django.shortcuts import render
from books.models import Book
from django.http import HttpResponse
from django.utils.safestring import mark_safe
import json

# def messenger(request):
# 	messages = Message.objects.filter(sender=request.user)
# 	if request.method=='POST':
# 		book = Book.objects.get(id=int(request.POST.get('book')))
# 		body = "Hi, I would like to rent " +book.title
# 		msg = Message(sender=request.user, receiver=book.owner, message=body)
# 		msg.save()
# 	return render(request, 'chats/index.html',{
# 		'messages':messages,
# 	})

def index(request):
    return render(request, 'chats/index.html', {})

def room(request, room_name):
     return render(request, 'chats/room.html', {
          'room_name_json': mark_safe(json.dumps(room_name))
     })