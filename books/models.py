from django.db import models
from django.contrib.auth.models import User
# from autoslug import AutoSlugField


class Genre(models.Model):
	title = models.CharField(max_length=60)
	slug = models.SlugField()
	
	class Meta:
		ordering = ('title',)

	def __str__(self):
		return self.title

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
	# genre = models.ForeignKey(Genre, on_delete=models.CASCADE, default=None)
	date = models.DateTimeField(auto_now_add=True)
	thumbnail = models.ImageField(default='default.png', blank = True)
	condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='new')
	availability = models.CharField(max_length=10, choices=AVAIL_CHOICES, default='rent')
	price = models.IntegerField(default=None)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
	stock = models.IntegerField(default=None)

	class Meta:
		ordering = ('title',)

	def __str__(self):
		return self.title

	def snippet(self):
		return self.description[:500]

	def read_more(self):
		return self.description[500:]

class BookGenre(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE, default=None)
	genre = models.ForeignKey(Genre, on_delete=models.CASCADE, default=None)

	class Meta:
		ordering = ('book',)

	def __str__(self):
		return str(self.book)

class ReadList(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
	books = models.ManyToManyField(Book, blank=True, help_text="books user have read")

	def __str__(self):
		return str(self.owner)

class BookRent(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
	books = models.ForeignKey(Book, on_delete=models.CASCADE, default=None, help_text="books user have rented")
	daterented = models.DateTimeField(blank=False)

	def __str__(self):
		return str(self.owner)