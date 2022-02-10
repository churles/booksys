from django.contrib import admin
from .models import Book, Genre, BookGenre, ReadList, BookRent, BookAvailability

admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(BookGenre)
admin.site.register(ReadList)
admin.site.register(BookRent)
admin.site.register(BookAvailability)