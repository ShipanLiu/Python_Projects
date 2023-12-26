from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS

# here we will create our own permissions:

# if you are admin: then you can do anything
# if you are not admin: then you only can read only:

class IsAdminOrReadOnly(BasePermission):
    #overwrite the method
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        # this means if "request.user" is set, then check "request.user.is_staff(means it can logi in the admin pannel)", -----> means it is admin
        return bool(request.user and request.user.is_staff)

