from rest_framework import permissions


class IsOwner (permissions.BasePermission):
    """Пользователь может изменять и удалять только свою рассылку"""
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user == view.get_object().owner
