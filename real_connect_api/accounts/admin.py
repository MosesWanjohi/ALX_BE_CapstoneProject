from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile, Role, UserRole
from followers.models import  Follower


# Register your models here.

#Registering the UserProfile model
class UserProfileAdmin(admin.ModelAdmin):
   list_display = ('user_name', 'company_name', 'location', 'website', 'specialization')
   search_fields = ('user_name', 'company_name', 'location', 'website', 'specialization')
   
   def get_roles(self, obj):
       return ", ".join([role.name for role in obj.roles.all()])
   get_roles.short_description = 'Roles' #Custom field name to show the roles in the admin panel

admin.site.register(UserProfile)

#Registering the CustomUser model with the UserAdmin

class CustomUserAdmin(UserAdmin):
   model = CustomUser
   list_display = ('email', 'username','is_staff', 'is_active', 'followers_count', 'following_count')
   search_fields = ('email', 'username',) #How an admin can search for a user
   list_filter = ('is_staff', 'is_active',)
   
   fieldsets = UserAdmin.fieldsets 
   
   def followers_count(self, obj):
      """
      Returns the number of followers for the given user.
      """
      return Follower.objects.filter(following=obj).count()
   
  
   
   def following_count(self, obj):
      """
      Returns the number of users the given user is following.
      """
      return Follower.objects.filter(follower=obj).count()
   
   followers_count.short_description = 'Followers'
   following_count.short_description = 'Following'

#Unregistering the default UserAdmin model if it exists
try:
   admin.site.unregister(CustomUser)
except admin.sites.NotRegistered:
   pass # default UserAdmin model does not exist

admin.site.register(CustomUser, CustomUserAdmin)

class UserRoleAdmin(admin.ModelAdmin):
   """
   Admin interface for UserRole model.
   """
   list_display = ('user', 'role')
   
admin.site.register(UserRole, UserRoleAdmin)

"""
Registering the Role model
"""
admin.site.register(Role)