from django.shortcuts import render
from .models import Message
from django.http import HttpResponse

def messenger(request):
	return HttpResponse("hello")
