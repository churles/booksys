from django.shortcuts import render, redirect
from .models import Review
from books.models import Book
from django.http import HttpResponse
from . import forms

def review_create(request, slug):
	book = Book.objects.get(slug=slug)
	if request.method == 'POST':
		form = forms.CreateReview(request.POST)
		if form.is_valid():
			#save to db
			instance = form.save(commit=False)
			instance.author = request.user
			instance.book = book
			instance.save()

			instance.slug = instance.slug +"-" +str(instance.id)
			instance.save()
			return redirect('books:list')
	else:
		form = forms.CreateReview()
		return render(request, 'reviews/review_create.html',{
			'form':form,
			'book': book
		})