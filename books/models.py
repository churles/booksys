from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField

CONDITION_CHOICES = (
    ('new','NEW'),
    ('good', 'GOOD'),
    ('used','USED'),
)
# AVAIL_CHOICES = (
# 	('rent','RENT'),
# 	('sale', 'SALE'),
# )

class Book(models.Model):
	title = models.CharField(max_length=60)
	author = models.CharField(max_length=60, default=None)
	slug = models.SlugField()
	description = models.TextField()
	date = models.DateTimeField(auto_now_add=True)
	thumbnail = models.ImageField(default='default.png', blank = True)
	condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='new')
	owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
	#availability = models.CharField(max_length=10, choices=AVAIL_CHOICES, default='rent')
	#add prices for rent and for sale

	def __str__(self):
		return self.title