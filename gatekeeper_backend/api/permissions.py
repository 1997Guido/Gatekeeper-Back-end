from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsEventOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(obj.EventOwner == request.user)


class IsUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(obj.user == request.user)


class IsImageOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(obj.Owner == request.user)
