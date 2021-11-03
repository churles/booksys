from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
	first_name = models.CharField(max_length=60)
	last_name = models.CharField(max_length=60)
	location = models.CharField(max_length=60)
	picture = models.ImageField(default='default.png', blank = True)
	account = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

	class Meta:
		ordering = ('last_name',)

	def __str__(self):
		return self.last_name