from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(BaseUserAdmin ):
   list_display = ('email', 'username', 'is_active', 'is_staff', 'profile_pic')

admin.site.register(CustomUser, CustomUserAdmin)