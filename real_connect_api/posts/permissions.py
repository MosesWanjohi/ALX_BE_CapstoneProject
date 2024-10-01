#Custom permissions class for posts

from rest_framework.permissions import BasePermission

class IsAuthorOrReadOnly(BasePermission):
    """
    Custom permission to only allow authors of a post to update or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        #Allow GET, HEAD or OPTIONS requests.(SAFE_METHODS)
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # Write permissions (update/delete)are only allowed to the author of a post.
        return request.user == obj.author
    
