from rest_framework import permissions


class IsUser (permissions.BasePermission):
    """Пользователь может просматривать, изменять и удалять только свой аккаунт"""
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user == view.get_object()
