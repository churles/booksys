from django.conf.urls import url
from . import views

app_name = 'books'

urlpatterns=[
	url(r'^$', views.books_list, name="list"),
	url(r'^create/$', views.books_create, name="create"),
	url(r'^reviewlike/$', views.reviewlike, name="reviewlike"),
    url(r'^(?P<slug>[\w-]+)/$', views.books_detail, name="detail"),
]