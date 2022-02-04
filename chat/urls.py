from django.urls import path
from django.conf.urls import url

from . import views 

app_name='chat'

urlpatterns = [
	path('', views.index, name='index'),
	path('usermessages/',views.user_messages, name='usermessages'),
	path('<str:room_name>/', views.room, name='room'),
    url(r'^room/delete/(?P<room_id>\d{1,10})/', views.room_delete, name="deleteRoom"),
]