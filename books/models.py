from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField

CONDITION_CHOICES = (
    ('new','NEW'),
    ('good', 'GOOD'),
    ('used','USED'),
)
AVAIL_CHOICES = (
	('rent','RENT'),
	('sale', 'SALE'),
)



class Book(models.Model):
	title = models.CharField(max_length=60)
	author = models.CharField(max_length=60, default=None)
	slug = models.SlugField()
	description = models.TextField()
	genre = models.CharField(max_length=60)
	date = models.DateTimeField(auto_now_add=True)
	thumbnail = models.ImageField(default='default.png', blank = True)
	condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='new')
	availability = models.CharField(max_length=10, choices=AVAIL_CHOICES, default='rent')
	price = models.CharField(max_length=60, default=None)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
	#add prices for rent and for sale

	class Meta:
		ordering = ('title',)

	def __str__(self):
		return self.title


class Genre(models.Model):
	title = models.CharField(max_length=60)
	slug = models.SlugField()
	
	class Meta:
		ordering = ('title',)

	def __str__(self):
		return self.title