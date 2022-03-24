from curses.ascii import HT
from tkinter import E
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth import login, logout
from . import forms
from .models import Following, Profile, UserPreference
from books.models import Book, ReadList
from django.contrib import messages
from django.contrib.auth.models import User
from books.models import Genre
from django.http import JsonResponse

import accounts

def signup_view(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			#login user
			login(request, user)
			messages.success(request, 'Welcome! Thanks for joining.')
			return redirect('books:list')
	else:
		form = UserCreationForm()
	return render(request,'accounts/signup.html',{
		'form':form
	})
	

def login_view(request):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			#login user
			user = form.get_user()
			login(request, user)
			return redirect('books:list')

	else:
		form = AuthenticationForm()
	return render(request, 'accounts/login.html',{
		'form':form
	})

def logout_view(request):
	if request.method == 'POST':
		logout(request)
		return redirect('accounts:login')

def create_view(request):
	if request.method == 'POST':
		form = forms.CreateProfile(request.POST, request.FILES)
		if form.is_valid():
			if request.POST.get('update') == "update":
				return redirect('accounts:update')
			else:
				instance = form.save(commit=False)
				instance.account = request.user
				instance.save()
				return redirect('accounts:create')
	else:
		profile = Profile.objects.filter(account=request.user)
		if not profile:
			form = forms.CreateProfile()
			return render(request, 'accounts/profile_create.html',{
				'form':form,
				'profile':profile
			})
		else:
			return redirect('accounts:update')

	return redirect('books:list')

def update_view(request):
		profile = Profile.objects.get(account=request.user)
		
		followers = Following.objects.filter(following=request.user)
		
		count = 0
		if Following.objects.filter(account=request.user):
			following = Following.objects.filter(account=request.user)[0]
			count = following.following.count()
			follows = following.following.all()
		

		read = ReadList.objects.get(owner=request.user)

		user = request.user

		listings_exist = []
		listings = []
		counter=0

		my_listings = Book.objects.filter(owner=request.user)
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


		if request.method == 'POST':
			profile.location = request.POST.get('location')
			profile.facebook = request.POST.get('facebook')
			profile.twitter = request.POST.get('twitter')
			profile.save()

			user.first_name = request.POST.get('fname')
			user.last_name = request.POST.get('lname')
			user.username = request.POST.get('uname')
			user.email = request.POST.get('email')
			user.save()

		# get user preference
		pref = ''
		if UserPreference.objects.get(account=request.user):
			pref = UserPreference.objects.get(account=request.user).genre.all()
			
		
		#get genre
		genres = Genre.objects.all()

		return render(request, 'accounts/personalinfo_update.html',{
			'profile':profile,
			'listings':listings,
			'listings_exist':listings_exist,
			'my_listings':my_listings,
			'followers':followers,
			'read':read,
			'listing':listing,
			'count':count,
			'follows':follows,
			'pref':pref,
			'genres':genres,
		})

def profile_update(request, profile_id):
	profile = Profile.objects.get(id=profile_id)

	if request.method == "POST":
		profile.picture = request.FILES.get('picture')
		profile.coverphoto = request.FILES.get('coverpicture')
		profile.save()

	return redirect('accounts:update')

def view_profile(request, user_id):
	owner = User.objects.get(id=user_id)
	owner_profile = Profile.objects.get(account=owner)
	profile = Profile.objects.get(account=request.user)

	follow = False

	followers = Following.objects.filter(following=owner)
	read = ReadList.objects.get(owner=owner)
	listing = Book.objects.filter(owner=owner)

	if not Following.objects.filter(account=request.user):
		follow = False
	else:
		user_following = Following.objects.get(account=request.user)
		for following in user_following.following.all():
			if following == owner:
				follow = True
	

	return render(request, 'accounts/view_profile.html',{
		'owner':owner,
		'owner_profile':owner_profile,
		'profile':profile,
		'followers':followers,
		'read':read,
		'listing':listing,
		'follow':follow
	})

def follow_view(request):
	ctr = False
	if request.method == 'POST':
		owner = User.objects.get(id=request.POST.get('user_id'))

		if not Following.objects.filter(account=request.user):
			user_following = Following.objects.create(account=request.user)
			user_following.save()
			user_following.following.add(owner)
		else:
			user_following = Following.objects.get(account=request.user)
			for following in user_following.following.all():
				if following == owner:
					user_following.following.remove(owner)
					ctr = True
			if ctr == False:
				user_following.following.add(owner)
		if request.POST.get('personalInfo') == 'true':
			return redirect('accounts:update')
		else:
			return redirect('accounts:view', user_id=owner.id)

def preference_view(request):
	if request.method == 'POST':
		genre = request.POST.getlist('genre[]')
		if UserPreference.objects.get(account=request.user):
			pref = UserPreference.objects.get(account=request.user)
			pref.genre.clear()
			for element in range(len(genre)):
				pref.genre.add(Genre.objects.get(id=int(genre[element])))
			pref.save()
		else:
			userPref = UserPreference.create(
				account=request.user
			)
			userPref.save()
			for element in range(len(genre)):
				userPref.genre.add(Genre.objects.get(id=int(genre[element])))
			userPref.save()
	if request.POST.get('ctr'):
		return redirect('accounts:update')
	else:
		return redirect('books:list')
