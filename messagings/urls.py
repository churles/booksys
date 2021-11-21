from django.conf.urls import url
from . import views

app_name = 'messagings'

urlpatterns=[
	url(r'^messenger/$', views.messenger, name="messenger"),
]