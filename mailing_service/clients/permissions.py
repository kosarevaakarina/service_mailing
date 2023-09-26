from rest_framework import permissions


class IsUser (permissions.BasePermission):
    """Пользователь может изменять и удалять только своего клиента"""
    def has_permission(self, request, view):
        if request.method in ['GET', 'POST']:
            return True
        if request.user.is_staff:
            return True
        return request.user == view.get_object().user
