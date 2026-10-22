from rest_framework import permissions

class PermisosBases(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return view.get_queryset().filter(pk = obj.pk).exists()
        
