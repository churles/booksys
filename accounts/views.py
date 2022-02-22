from curses.ascii import HT
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth import login, logout
from . import forms
from .models import Profile
from django.contrib import messages

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
		user = request.user
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

			
		return render(request, 'accounts/personalinfo_update.html',{
			'profile':profile
		})

def profile_update(request, profile_id):
	profile = Profile.objects.get(id=profile_id)
	if request.method == "POST":
		profile.picture = request.FILES.get('picture')
		profile.coverphoto = request.FILES.get('coverpicture')
		profile.save()

	return redirect('accounts:update')