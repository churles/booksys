from django.shortcuts import render, redirect
from .models import Book, Genre, BookGenre
from reviews.models import Review, ReviewLike
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms
from array import array
from django.http import JsonResponse

@login_required(login_url="/accounts/login/")
def books_create(request):
	if request.method == 'POST':
		form = forms.CreateBook(request.POST, request.FILES)
		if form.is_valid():
			# save to db
			instance = form.save(commit=False)
			instance.owner = request.user
			instance.save()
			bookgenres = request.POST.getlist('genre[]')
			for element in range(len(bookgenres)):
				bg = BookGenre()
				bg.book = Book.objects.get(id = instance.id)
				bg.genre = Genre.objects.get(id=int(bookgenres[element]))
				bg.save()
			return redirect('books:list')
	else:
		genres = Genre.objects.all()
		form = forms.CreateBook()
	return render(request, 'books/book_create.html',{
		'form':form,
		'genres':genres
	})

def books_list(request):
	books = Book.objects.all().order_by('date')
	return render(request, 'books/book_list.html',{
		'books':books
	})

def books_detail(request, slug):
	book = Book.objects.get(slug=slug)
	reviews = Review.objects.all().order_by('datetime')
	reviewlike = ReviewLike.objects.all()

	return render(request, 'books/book_detail.html',{
		'book':book,
		'reviews':reviews,
		'reviewlike':reviewlike
	})

def reviewlike(request):
	if request.method == 'POST':
		review = request.POST.get('review_id')
		owner = request.POST.get('owner')
		slug = request.POST.get('slug')
		review_instance = Review.objects.get(id=int(review))
		owner_instance = request.user

		rl = ReviewLike.objects.all()

		if not rl:
			like = ReviewLike(review=review_instance,owner=owner_instance)
			like.save()
		else:
			rl = ReviewLike.objects.filter(review=review_instance, owner=owner_instance)
			if not rl:
				like = ReviewLike(review=review_instance,owner=owner_instance)
				like.save()
			else:
				rl.delete()
		
		likes = ReviewLike.objects.filter(review=review_instance).count()
		data = {
			'likes': likes,
		}
		return JsonResponse(data, safe=False)

	return redirect('books:detail', slug=slug)