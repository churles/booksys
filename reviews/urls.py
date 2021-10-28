from django.conf.urls import url
from . import views

app_name = 'reviews'

urlpatterns=[
	#url(r'^create/', views.review_create, name="create"),
    url(r'^(?P<slug>[\w-]+)/create/', views.review_create, name="create"),
]