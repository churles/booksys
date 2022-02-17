from django.contrib import admin
from .models import Book, Genre, ReadList, BookRent, BookAvailability, RelatedImage

admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(ReadList)
admin.site.register(BookRent)
admin.site.register(BookAvailability)
admin.site.register(RelatedImage)