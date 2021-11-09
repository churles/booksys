from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
	location = models.CharField(max_length=60)
	picture = models.ImageField(default='default.png', blank = True)
	account = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

	class Meta:
		ordering = ('location',)

	def __str__(self):
		return self.location