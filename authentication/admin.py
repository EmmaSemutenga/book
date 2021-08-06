from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UAdmin
from .models import User

class UserAdmin(UAdmin):
    list_display = ('photo', 'username')



# Register your models here.
admin.site.register(User, UserAdmin)