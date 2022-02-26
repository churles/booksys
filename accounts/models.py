from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
	location = models.CharField(max_length=60)
	facebook = models.CharField(max_length=60, blank=True)
	twitter = models.CharField(max_length=60, blank=True)
	picture = models.ImageField(default='default.png', blank = True)
	coverphoto = models.ImageField(default='default.png', blank = True)
	account = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

	class Meta:
		ordering = ('account',)

	def __str__(self):
		return str(self.account)

class Following(models.Model):
	account = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
	following = models.ManyToManyField(User, blank=True, related_name="users_following")

	class Meta:
		ordering = ('account',)

	def __str__(self):
		return str(self.account)