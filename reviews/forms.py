from django import forms
from . import models

class CreateReview(forms.ModelForm):
	class Meta:
		model = models.Review
		fields = ['title','body','slug']
		
		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control'}),
			'body': forms.TextInput(attrs={'class': 'form-control'}),
			'slug': forms.HiddenInput(),
		}