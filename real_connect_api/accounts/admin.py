from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile

# Register your models here.
#Registering the CustomUser model with the UserAdmin

class CustomUserAdmin(UserAdmin):
   model = CustomUser
   list_display = ('email', 'username','is_staff', 'is_active',)
   search_fields = ('email', 'username',) #How an admin can search for a user
   list_filter = ('is_staff', 'is_active',)
   
   fieldsets = UserAdmin.fieldsets 
   
admin.site.register(CustomUser, CustomUserAdmin)

#Registering the UserProfile model
class UserProfileAdmin(admin.ModelAdmin):
   list_display = ('user', 'company_name', 'location', 'website', 'specialization')
   search_fields = ('user_name', 'company_name', 'location', 'website', 'specialization')
   
   def get_roles(self, obj):
       return ", ".join([role.name for role in obj.roles.all()])
   get_roles.short_description = 'Roles' #Custom column name to show the roles in the admin panel

admin.site.register(UserProfile)