from django import forms
from . import models

class CreateBook(forms.ModelForm):
	class Meta:
		model = models.Book
		fields = ['title','author','description', 'genre','slug','thumbnail','condition', 'availability', 'price']

		# GENRE_CHOICES = []
		# genres = Genre.objects.all()

		# for genre in genres:
		# 	GENRE_CHOICES.append((genre.title.lower(),genre.title))
		# GENRE_CHOICES = tuple(GENRE_CHOICES)

		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control'}),
			'author': forms.TextInput(attrs={'class': 'form-control'}),
			'description': forms.Textarea(attrs={'class': 'form-control'}),
			# 'genre': forms.Select(attrs={'class': 'form-control'}, choices=GENRE_CHOICES),
			'genre': forms.TextInput(attrs={'class': 'form-control'}),
			'slug': forms.HiddenInput(),
			'thumbnail': forms.FileInput(attrs={'class': 'form-control-file'}),
			'condition': forms.Select(attrs={'class': 'form-control'}),
			'availability': forms.Select(attrs={'class': 'form-control'}),
			'price': forms.TextInput(attrs={'class': 'form-control'}),
		}