from django.shortcuts import render, redirect
from .models import Review
from books.models import Book
from django.http import HttpResponse
from . import forms
from django.contrib.auth.decorators import login_required

@login_required(login_url="/accounts/login/")
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
			return redirect('books:detail', slug=slug)
	else:
		form = forms.CreateReview()
		return render(request, 'reviews/review_create.html',{
			'form':form,
			'book': book,
		})

def review_update(request, review_id, slug):
	review = Review.objects.get(id=review_id)
	form = forms.CreateReview(request.POST or None, instance=review)
	if form.is_valid():
		form.save()
		return redirect('books:detail', slug=slug)

	return render(request, 'reviews/review_update.html',{
		'review':review,
		'form':form
	})
