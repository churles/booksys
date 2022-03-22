from django.contrib import admin
from .models import Profile, Following, UserPreference

admin.site.register(Profile)
admin.site.register(Following)
admin.site.register(UserPreference)