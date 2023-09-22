from rest_framework import permissions


class IsEmployeeOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
            if request.user.is_authenticated:
                if request.method in permissions.SAFE_METHODS:
                    return True

                return request.user.role.role_type == 'employee'

            return False
    

class IsCreatorOrReciever(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.recievers.all() or obj.creator.pk == request.user.pk
    

class IsRecieverAndRole(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role.pk in obj.status.roles.all() and request.user.pk == obj.recievers.all().last().pk