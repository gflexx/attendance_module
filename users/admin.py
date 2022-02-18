from django.contrib.auth.models import Group
from django.contrib.admin import AdminSite
from django.contrib import admin

from .models import User

# admin site tiles and header
AdminSite.site_title = 'Attandance Module Admin'
AdminSite.site_header = 'Attandance Module Admin Panel'


admin.site.register(User)
admin.site.unregister(Group)