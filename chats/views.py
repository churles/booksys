from django.shortcuts import render
from .models import Message
from books.models import Book
from django.http import HttpResponse

def messenger(request):
	messages = Message.objects.filter(sender=request.user)
	if request.method=='POST':
		book = Book.objects.get(id=int(request.POST.get('book')))
		body = "Hi, I would like to rent " +book.title
		msg = Message(sender=request.user, receiver=book.owner, message=body)
		msg.save()
	return render(request, 'chats/index.html',{
		'messages':messages,
	})