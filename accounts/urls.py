from django.conf.urls import url
from . import views

app_name = 'accounts'

urlpatterns = [
	url(r'^signup/$', views.signup_view, name="signup"),
	url(r'^login/$', views.login_view, name="login"),
	url(r'^logout/$', views.logout_view, name="logout"),
	url(r'^create/$', views.create_view, name="create"),
	url(r'^update/$', views.update_view, name="update"),
	url(r'^follow/$', views.follow_view, name="follow"),
	url(r'^view/profile/(?P<user_id>\d{1,10})/$', views.view_profile, name="view"),
	url(r'^profile/update/(?P<profile_id>\d{1,10})/$', views.profile_update, name="profile_update"),

]