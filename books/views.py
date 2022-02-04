from curses.ascii import HT
from turtle import title
from django import http
from django.shortcuts import render, redirect
from .models import Book, BookRent, Genre, BookGenre, ReadList
from reviews.models import Review, ReviewLike
from accounts.models import Profile
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms
from array import array
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator

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
			return redirect('books:detail', slug=instance.slug, page_id=1)
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

def books_detail(request, slug, page_id):
	review_id = ''
	book = Book.objects.get(slug=slug)
	reviews = Review.objects.filter(book=book).order_by('datetime')
	reviewlike = ReviewLike.objects.all()
	readlist = ReadList.objects.filter(owner=request.user)
	bookrent = BookRent.objects.filter(owner=request.user, books=book)
	review_exist = Review.objects.filter(author=request.user, book=book)

	if review_exist.exists():
		review_id = Review.objects.get(author=request.user, book=book).id

	paginator_review = Paginator(reviews, 2)
	page = paginator_review.get_page(page_id)
		
	return render(request, 'books/book_detail.html',{
		'book':book,
		'reviews':reviews,
		'count':paginator_review.count,
		'reviewlike':reviewlike,
		'readlist':readlist,
		'bookrent':bookrent,
		'review_exist':review_exist,
		'review_id':review_id,
		'page':page,
	})

def reviewlike(request):
	slug = ''
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

@login_required(login_url="/accounts/login/")
def library(request):
	tab = ''
	books = []
	if request.method == 'POST':
		tab = request.POST.get('tab_name')
	my_listings = Book.objects.filter(owner=request.user)
	username = request.user.username
	profile = Profile.objects.get(account=request.user)
	readlist = ReadList.objects.filter(owner=request.user)
	bookrent = BookRent.objects.filter(owner=request.user)
	for rented in bookrent:
		books.append(rented.books)
	
	return render(request, 'books/book_library.html',{
		'my_listings':my_listings,
		'username':username,
		'profile':profile,
		'readlist':readlist,
		'bookrent':bookrent,
		'tab':tab,
		'books':books
	})

def read(request):
	if request.method == 'POST':
		book = Book.objects.get(id=request.POST.get('book'))
		slug = request.POST.get('slug')
		read = ReadList.objects.filter(owner=request.user)
		if not read:
			new_read = ReadList(owner=request.user)
			new_read.save()
			new_read.books.add(book)
		
			return redirect('books:detail', slug=slug, page_id=1)
		else:
			read = ReadList.objects.get(owner=request.user)
			read.books.add(book)
			return redirect('books:detail', slug=slug, page_id=1)

def book_update(request, book_id):
	book = Book.objects.get(id=book_id)
	form = forms.CreateBook(request.POST or None, instance=book)
	
	if form.is_valid():
		form.save()
		return redirect('books:detail', slug=book.slug, page_id=1)

	return render(request, 'reviews/review_update.html',{
		'book':book,
		'form':form
	})

def book_delete(request, book_id):
	book = Book.objects.get(id=int(book_id))
	title = book.title
	book.delete()
	messages.success(request, title +'has been deleted from your book listings.')
	return redirect('books:library')

def read_delete(request, book_id):
	book = Book.objects.get(id=int(book_id))
	title = book.title
	read = ReadList.objects.get(owner=request.user, books=book)
	read.books.remove(book)
	messages.success(request, title + ' has been deleted from your Have Read list.')
	messages.info(request, ' go to tab2')
	return redirect('books:library')