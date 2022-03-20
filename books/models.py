from distutils.command.upload import upload
from pickle import TRUE
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
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
	slug = models.SlugField(blank=TRUE, max_length=200)
	synopsis = models.TextField()
	note = models.TextField(blank=True)
	date = models.DateTimeField(auto_now_add=True)
	thumbnail = models.ImageField(default='default.png', blank = True)
	genre = models.ManyToManyField(Genre, blank=True)
	condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='new')
	qr_code = models.ImageField(upload_to='qr_codes', blank=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

	class Meta:
		ordering = ('title',)

	def __str__(self):
		return self.title

	def snippet(self):
		return self.synopsis[:500]

	def read_more(self):
		return self.synopsis[500:]

	def note_snippet(self):
		return self.note[:500]

	def note_read_more(self):
		return self.note[500:]
		
	def save(self, *args, **kwargs):
		qrcode_img = qrcode.make(self.slug)
		canvas = Image.new('RGB', (qrcode_img.pixel_size, qrcode_img.pixel_size), 'white')
		draw = ImageDraw.Draw(canvas)
		canvas.paste(qrcode_img)
		fname = f'qr_code-{self.slug}'+'.png'
		buffer = BytesIO()
		canvas.save(buffer,'PNG')
		self.qr_code.save(fname, File(buffer), save=False)
		canvas.close()
		super().save(*args, **kwargs)

class BookAvailability(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE, default=None)
	availability = models.CharField(max_length=10, choices=AVAIL_CHOICES, default='rent')
	daterange = models.CharField(max_length=10, default="30", blank=True)
	price = models.IntegerField(default=None, blank=True)
	stock = models.IntegerField(default=None)

	class Meta:
		ordering = ('book',)

	def __str__(self):
		return str(self.book)

class RelatedImage(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE, default=None)
	image = models.ImageField(default=None, blank = True)

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

class Banner(models.Model):
	name =  models.CharField(max_length=10, blank=True)
	picture = models.ImageField(default=None, blank = True)
	caption_title =  models.CharField(max_length=100, blank=True)
	caption = models.TextField(blank=True)
	priority = models.CharField(max_length=10, blank=True)
	active = models.CharField(max_length=10, blank=True, default="false")

	def __str__(self):
		return str(self.name)
