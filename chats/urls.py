from django.conf.urls import url, re_path
from . import views

app_name = 'chats'

urlpatterns=[
	url(r'^$', views.index, name="index"),
	re_path(r'^(?P<room_name>[^/]+)/$', views.room, name="room"),
]