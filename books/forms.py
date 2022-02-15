from django import forms
from . import models

class CreateBook(forms.ModelForm):
	class Meta:
		model = models.Book
		fields = ['title','author','synopsis','slug','thumbnail','condition']

		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control'}),
			'author': forms.TextInput(attrs={'class': 'form-control'}),
			'synopsis': forms.Textarea(attrs={'class': 'form-control'}),
			'slug': forms.HiddenInput(),
			'thumbnail': forms.FileInput(attrs={'class': 'form-control-file'}),
			'condition': forms.Select(attrs={'class': 'form-control'})
		}