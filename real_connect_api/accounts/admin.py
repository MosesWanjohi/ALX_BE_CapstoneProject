from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile

# Register your models here.
#Registering the CustomUser model with the UserAdmin
class CustomUserAdmin(UserAdmin):
   model = CustomUser
   list_display = ('email', 'username','is_staff', 'is_active',)
   fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'profile_pic', 'location', 'website', 'cover_pic')}),
      
   )
admin.site.register(CustomUser, CustomUserAdmin)

#Registering the UserProfile model
class UserProfileAdmin(admin.ModelAdmin):
   list_display = ('user', 'role')
   
admin.site.register(UserProfile)