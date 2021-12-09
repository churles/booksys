from django import forms
from . import models

class CreateBook(forms.ModelForm):
	class Meta:
		model = models.Book
		fields = ['title','author','description','slug','thumbnail','condition', 'availability', 'price', 'stock']

		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control'}),
			'author': forms.TextInput(attrs={'class': 'form-control'}),
			'description': forms.Textarea(attrs={'class': 'form-control'}),
			'slug': forms.HiddenInput(),
			'thumbnail': forms.FileInput(attrs={'class': 'form-control-file'}),
			'condition': forms.Select(attrs={'class': 'form-control'}),
			'availability': forms.Select(attrs={'class': 'form-control'}),
			'price': forms.TextInput(attrs={'class': 'form-control'}),
			'stock': forms.TextInput(attrs={'class': 'form-control'}),
		}

class CreateBookGenre(forms.ModelForm):
	class Meta:
		model = models.BookGenre
		fields = ['book','genre']