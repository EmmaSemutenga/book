from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UAdmin
from .models import User

class UserAdmin(UAdmin):
    list_display = ('username', 'photo')



# Register your models here.
admin.site.register(User, UserAdmin)