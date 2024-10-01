from django.contrib import admin
from .models import Post

#Customizing the PostAdmin
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at', 'updated_at')#Display fields for the Post model in list view
    search_fields = ('title', 'content', 'author__username') #Search by title, content or author

    list_filter = ('author',) #Filter posts by author

# Register your models here.
admin.site.register(Post, PostAdmin)