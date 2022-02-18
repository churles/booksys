from curses.ascii import HT
from enum import unique
from pickle import TRUE
from turtle import title
from wsgiref.util import request_uri
from django import http
from django.shortcuts import render, redirect
from .models import Book, BookRent, Genre, ReadList, BookAvailability, RelatedImage
from reviews.models import Review, ReviewLike
from accounts.models import Profile
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms
from array import array
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User

@login_required(login_url="/accounts/login/")
def books_create(request):
	if request.method == 'POST':
		book = Book.objects.create(
			title=request.POST.get('title'), 
			author=request.POST.get('author'),
			synopsis=request.POST.get('synopsis'),
			note=request.POST.get('note'),
			thumbnail=request.FILES.get('thumbnail'),
			condition=request.POST.get('condition'),
			owner=request.user
			)
		book.save()
		book.slug = request.POST.get('slug') + str(book.id)

		bookgenres = request.POST.getlist('genre[]')
		for element in range(len(bookgenres)):
			book.genre.add(Genre.objects.get(id=int(bookgenres[element])))

		book.save()

		relatedpics = request.FILES.getlist('relatedpic[]')
		for relatedpic in relatedpics:
			pics = RelatedImage.objects.create(
				book=book,
				image=relatedpic 
			)
			pics.save()
		
		
		return redirect('books:availability', book_id=book.id)
	else:
		genres = Genre.objects.all()
		form = forms.CreateBook()
	return render(request, 'books/book_create.html',{
		'form':form,
		'genres':genres
	})

def books_availability(request, book_id):
	book = Book.objects.get(id=book_id)
	if request.method == 'POST':
		book_avail = BookAvailability.objects.create(
			book=book,
			availability=request.POST.get('availability'),
			price=request.POST.get('price'),
			stock=request.POST.get('stock')
		)
		book_avail.save()
		if(book_avail.availability == "rent"):
			book_avail.daterange = request.POST.get('daterange')
			book_avail.save()
		return redirect('books:finish', book_id=book.id, book_avail_id=book_avail.id, status="create")

	return render(request, 'books/book_availability.html',{
		'book':book,
	})

def books_finish(request, book_id, book_avail_id, status):
	book = Book.objects.get(id=book_id)
	book_avail = BookAvailability.objects.get(id=book_avail_id)

	return render(request, 'books/book_finish.html',{
		'book':book,
		'book_avail':book_avail,
		'status':status
	})

def books_list(request):
	books = Book.objects.all().order_by('date')
	profile = ""
	if request.user.is_authenticated:
		profile = Profile.objects.get(account = request.user)
	return render(request, 'books/book_list.html',{
		'books':books,
		'profile':profile
	})

def books_detail(request, slug, page_id):
	review_id = ''
	book = Book.objects.get(slug=slug)
	book_avail = BookAvailability.objects.get(book=book)
	reviews = Review.objects.filter(book=book).order_by('datetime')
	reviewlike = ReviewLike.objects.all()
	readlist = ReadList.objects.filter(owner=request.user)
	bookrent = BookRent.objects.filter(owner=request.user, books=book)
	review_exist = Review.objects.filter(author=request.user, book=book)

	if review_exist.exists():
		review_id = Review.objects.get(author=request.user, book=book).id

	paginator_review = Paginator(reviews, 10)
	page = paginator_review.get_page(page_id)
		
	return render(request, 'books/book_detail.html',{
		'book':book,
		'book_avail':book_avail,
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

	return redirect('books:detail', slug=slug, page_id=1)

@login_required(login_url="/accounts/login/")
def library(request):
	tab = ''
	books = []
	listings = []
	listings_exist = []
	counter = 0
	if request.method == 'POST':
		tab = request.POST.get('tab_name')
	my_listings = Book.objects.filter(owner=request.user)
	username = request.user.username
	profile = Profile.objects.get(account=request.user)
	readlist = ReadList.objects.filter(owner=request.user)
	bookrent = BookRent.objects.filter(owner=request.user)

	for my_listing in my_listings:
		ctr = False
		# if listing is empty
		if not listings: 
			listings.append(my_listing)
		# listing is not empty
		else:
			for listing in listings:
				if listing.title == my_listing.title and listing.author == my_listing.author:
					ctr = True
					listings_exist.append(my_listing)
					counter += 1
					break
				else:
					ctr = False
			if ctr == False:
				listings.append(my_listing)

	for rented in bookrent:
		books.append(rented.books)


	return render(request, 'books/book_library.html',{
		'my_listings':my_listings,
		'username':username,
		'profile':profile,
		'readlist':readlist,
		'bookrent':bookrent,
		'tab':tab,
		'books':books,
		'listings':listings,
		'listings_exist':listings_exist,
		'counter':counter
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

def book_update_prev(request, book_id, status):
	book = Book.objects.get(id=book_id)
	genres = Genre.objects.all()

	if request.method == "POST":
		book.title=request.POST.get('title')
		book.author=request.POST.get('author')
		book.synopsis=request.POST.get('synopsis')
		book.note=request.POST.get('note')
		book.thumbnail=request.FILES.get('thumbnail')
		book.condition=request.POST.get('condition')
		book.slug = ""
		book.save()
		book.slug = request.POST.get('slug') + str(book.id)
		book.genre.clear()

		bookgenres = request.POST.getlist('genre[]')
		for element in range(len(bookgenres)):
			book.genre.add(Genre.objects.get(id=int(bookgenres[element])))

		book.save()

		if status == "previous":
			return redirect('books:availability', book_id=book_id)
		else:
			return redirect('books:avail_update', book_id=book.id)
	return render(request, 'books/book_update.html',{
		'book':book,
		'genres':genres,
		'status':status
	})

def book_update(request, book_id):
	book = Book.objects.get(id=book_id)
	genres = Genre.objects.all()

	if request.method == "POST":
		book.title=request.POST.get('title')
		book.author=request.POST.get('author')
		book.synopsis=request.POST.get('synopsis')
		book.note=request.POST.get('note')
		book.thumbnail=request.FILES.get('thumbnail')
		book.condition=request.POST.get('condition')
		
		book.save()
		book.slug = request.POST.get('slug') + str(book.id)
		book.genre.clear()

		bookgenres = request.POST.getlist('genre[]')
		for element in range(len(bookgenres)):
			book.genre.add(Genre.objects.get(id=int(bookgenres[element])))

		book.save()

		
		return redirect('books:avail_update', book_id=book.id)
		

	return render(request, 'books/book_update.html',{
		'book':book,
		'genres':genres
	})

def book_availability_update(request, book_id):
	book = Book.objects.get(id=book_id)
	book_avail = BookAvailability.objects.get(book=book)

	if request.method == 'POST':
		book_avail.availability=request.POST.get('availability')
		book_avail.price=request.POST.get('price')
		book_avail.stock=request.POST.get('stock')
		
		book_avail.save()

		if(book_avail.availability == "rent"):
			book_avail.daterange = request.POST.get('daterange')
			book_avail.save()

		return redirect('books:finish', book_id=book.id, book_avail_id=book_avail.id, status="update")

	return render(request, 'books/book_availability_update.html',{
		'book':book,
		'book_avail':book_avail
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

def listings(request, book_id, owner_id):
	if int(owner_id) == 0:
		owner = ""
	else:
		owner = User.objects.get(id = int(owner_id))
	
	book = Book.objects.get(id= int(book_id))
	book_avail = BookAvailability.objects.all()

	if not owner:
		similar = Book.objects.filter(title=book.title, author=book.author)
	else:
		similar = Book.objects.filter(title=book.title, author=book.author, owner = owner)

	return render(request, 'books/book_other_listings.html',{
		'title':book.title,
		'original':book,
		'book_avail':book_avail,
		'similar':similar,
		'owner':owner
	})