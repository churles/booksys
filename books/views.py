from django.shortcuts import get_object_or_404, render, redirect
from .models import Book, BookRent, Genre, ReadList, BookAvailability, RelatedImage, Banner
from reviews.models import Review, ReviewLike
from accounts.models import Profile, UserPreference
from chat.models import PublicChatRoom
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic import ListView

@login_required(login_url="/accounts/login/")
def books_create(request):
	profile = ""
	if request.user.is_authenticated:
		profile = Profile.objects.get(account = request.user)

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
		'genres':genres,
		'profile':profile
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
	fyp = []
	banners = Banner.objects.filter(active="true").order_by('priority')
	counter = []
	ctr = 0
	
	while ctr < banners.count():
		counter.append(ctr)
		ctr = ctr + 1
	
	# check userpreference in terms of genre
	if request.user.is_authenticated:
		if UserPreference.objects.filter(account=request.user):
			preference = UserPreference.objects.get(account=request.user)
			for p in preference.genre.all():
				fyp.append(p)

	# get all genre for setting preference 
	genres = Genre.objects.all()

	# check if user is authenticated
	if request.user.is_authenticated:
		profile = Profile.objects.get(account = request.user)

	# get messages
	chat_room = PublicChatRoom.objects.filter(users=request.user)
	room = chat_room.exclude(deleted_by=request.user)
	roomcount = 0
	if not room:
		roomcount = 0
	else:
		roomcount = room.count()

	return render(request, 'books/book_list.html',{
		'books':books,
		'profile':profile,
		'banners':banners,
		'counter':counter,
		'fyp':fyp,
		'genres':genres,
		'roomcount':roomcount,
	})

def books_detail(request, slug, page_id):
	review_id = ''
	profile = ""
	if request.user.is_authenticated:
		profile = Profile.objects.get(account = request.user)

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
		'profile':profile
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
		books.append(BookAvailability.objects.get(book = rented.books))

	# get messages
	chat_room = PublicChatRoom.objects.filter(users=request.user)
	room = chat_room.exclude(deleted_by=request.user)
	roomcount = 0
	if not room:
		roomcount = 0
	else:
		roomcount = room.count()

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
		'counter':counter,
		'roomcount':roomcount,
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
	profile = Profile.objects.get(account=request.user)

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
		'status':status,
		'profile':profile
	})

def book_update(request, book_id):
	book = Book.objects.get(id=book_id)
	genres = Genre.objects.all()
	profile = Profile.objects.get(account=request.user)

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
		'genres':genres,
		'profile':profile,
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
	profile = ""
	if request.user.is_authenticated:
		profile = Profile.objects.get(account = request.user)

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
		'owner':owner,
		'profile':profile
	})

def render_bookInfoView(request, *args, **kwargs):
	pk = kwargs.get('book_id')
	book = get_object_or_404(Book, pk=pk)
	avail = BookAvailability.objects.get(book=book)
	counter = []
	ctr = 1
	while ctr <= avail.stock:
		counter.append(ctr)
		ctr = ctr + 1


	template_path = 'books/book_info.html'
	context = {'book': book, 'avail':avail,'counter':counter}
	# Create a Django response object, and specify content_type as pdf
	response = HttpResponse(content_type='application/pdf')
	# if download response['Content-Disposition'] = 'attachment; filename="report.pdf"'
	response['Content-Disposition'] = 'filename="report.pdf"'
	# find the template and render it.
	template = get_template(template_path)
	html = template.render(context)

	# create a pdf
	pisa_status = pisa.CreatePDF(
	html, dest=response)
	# if error then show some funy view
	if pisa_status.err:
		return HttpResponse('We had some errors <pre>' + html + '</pre>')
	return response