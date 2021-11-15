from django.db import models
from django.contrib.auth.models import User
from books.models import Book

class Review(models.Model):
	title = models.CharField(max_length=60)
	slug = models.SlugField()
	body = models.TextField()
	datetime = models.DateTimeField(auto_now_add=True)
	book = models.ForeignKey(Book, on_delete=models.CASCADE, default=None)
	author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

	def __str__(self):
		return self.title

	def snippet(self):
		return self.body[:250]

	def read_more(self):
		return self.body[250:]
