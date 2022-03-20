from django.urls import re_path as url
from . import views

app_name = 'searches'

urlpatterns=[
	url(r'^$', views.search, name="search"),
]