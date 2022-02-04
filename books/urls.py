from django.conf.urls import url
from . import views

app_name = 'books'

urlpatterns=[
	url(r'^$', views.books_list, name="list"),
	url(r'^create/$', views.books_create, name="create"),
	url(r'^reviewlike/$', views.reviewlike, name="reviewlike"),
	url(r'^library/$', views.library, name="library"),
	url(r'^read/$', views.read, name="read"),
    url(r'^update/(?P<book_id>\d{1,10})/$', views.book_update, name="update"),
    url(r'^delete/(?P<book_id>\d{1,10})/$', views.book_delete, name="delete"),
    url(r'^read/delete/(?P<book_id>\d{1,10})/$', views.read_delete, name="deleteRead"),
    url(r'^(?P<slug>[\w-]+)/(?P<page_id>\d{1,10})/$', views.books_detail, name="detail"),
]