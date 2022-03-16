from django.urls import path, re_path as url

from . import views 

app_name='chat'

urlpatterns = [
	path('', views.index, name='index'),
	path('usermessages/',views.user_messages, name='usermessages'),
	path('bookmessages/',views.book_messages, name='bookmessages'),
	path('<str:room_name>/', views.room, name='room'),
    url(r'^room/delete/(?P<room_id>\d{1,10})/', views.room_delete, name="deleteRoom"),
]