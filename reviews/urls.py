from django.urls import path, re_path as url
from . import views

app_name = 'reviews'

urlpatterns=[
	#url(r'^create/', views.review_create, name="create"),
    url(r'^update/(?P<review_id>\d{1,10})/(?P<slug>[\w-]+)/$', views.review_update, name="update"),
    url(r'^(?P<slug>[\w-]+)/create/', views.review_create, name="create"),
    url(r'^delete/(?P<review_id>\d{1,10})/(?P<slug>[\w-]+)/$', views.review_delete, name="delete"),
]