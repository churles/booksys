from django import forms
from . import models

class CreateProfile(forms.ModelForm):
	class Meta:
		model = models.Profile
		fields = ['location','picture']

		widgets = {
			'location':forms.TextInput(attrs={'class': 'form-control'}),
			'picture':forms.FileInput(attrs={'class': 'form-control-file'}),
		}