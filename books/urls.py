from django.conf.urls import url
from . import views

app_name = 'books'

urlpatterns=[
	url(r'^$', views.books_list, name="list"),
	url(r'^create/$', views.books_create, name="create"),
	url(r'^reviewlike/$', views.reviewlike, name="reviewlike"),
	url(r'^library/$', views.library, name="library"),
	url(r'^read/$', views.read, name="read"),
	url(r'^bookinfo/(?P<book_id>\d{1,10})/$', views.render_bookInfoView, name="bookInfo"),
	url(r'^listings/(?P<book_id>\d{1,10})/(?P<owner_id>\d{1,10})/$', views.listings, name="listings"),
	url(r'^availability/(?P<book_id>\d{1,10})/$', views.books_availability, name="availability"),
    url(r'^availability/update/(?P<book_id>\d{1,10})/$', views.book_availability_update, name="avail_update"),
    url(r'^delete/(?P<book_id>\d{1,10})/$', views.book_delete, name="delete"),
    url(r'^read/delete/(?P<book_id>\d{1,10})/$', views.read_delete, name="deleteRead"),
    url(r'^update/(?P<book_id>\d{1,10})/$', views.book_update, name="update"),
	url(r'^updatePrev/(?P<book_id>\d{1,10})/(?P<status>[\w-]+)/$', views.book_update_prev, name="updatePrev"),
	url(r'^finish/(?P<book_id>\d{1,10})/(?P<book_avail_id>\d{1,10})/(?P<status>[\w-]+)/$', views.books_finish, name="finish"),
    url(r'^(?P<slug>[\w-]+)/(?P<page_id>\d{1,10})/$', views.books_detail, name="detail"),
]