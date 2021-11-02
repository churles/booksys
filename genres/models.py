from django.db import models

class Genre(models.Model):
	title = models.CharField(max_length=60)
	slug = models.SlugField()
	
	def __str__(self):
		return self.title
