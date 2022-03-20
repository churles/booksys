from django.shortcuts import render
from django.http import HttpResponse
from books.models import Book, Genre

# Create your views here.

def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        books = Book.objects.filter(title__contains=searched)
        authors = Book.objects.filter(author__contains=searched)
        # fix genre search
        genres = Genre.objects.filter(title__contains=searched)
        if genres:
            genres = Book.objects.filter(genre__id=genres[0].id)
        else:
            genres = ''
        return render(request, 'searches/search.html',{
            'searched':searched,
            'books':books,
            'authors':authors,
            'genres':genres
        })
    else:
        return render(request, 'searches/search.html',{

        })