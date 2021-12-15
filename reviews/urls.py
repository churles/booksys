from django.conf.urls import url
from django.urls import path    
from . import views

app_name = 'reviews'

urlpatterns=[
	#url(r'^create/', views.review_create, name="create"),
    url(r'^update/(?P<review_id>\d{1,10})/(?P<slug>[\w-]+)/$', views.review_update, name="update"),
    url(r'^(?P<slug>[\w-]+)/create/', views.review_create, name="create"),
]