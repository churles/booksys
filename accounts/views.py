from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth import login, logout
from . import forms
from .models import Profile

def signup_view(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			#login user
			login(request, user)
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
	user = request.user.id
	profile = Profile.objects.get(account=user)
	if profile != None:
		form = forms.CreateProfile()
		return render(request, 'accounts/profile_create.html',{
			'form':form,
			'profile':profile
		})


	# if request.method == 'POST':
	# 	form = forms.CreateProfile(request.POST, request.FILES)
	# 	if form.is_valid():
	# 		instance = form.save(commit=False)
	# 		instance.account = request.user
	# 		instance.save()
	# 		return redirect('accounts:create')
	# else:
	# 	form = forms.CreateProfile()
	# return render(request, 'accounts/profile_create.html',{
	# 	'form':form
	# })