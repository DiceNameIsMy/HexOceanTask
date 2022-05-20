from rest_framework.permissions import BasePermission


class HasAccountTier(BasePermission):
    message = "User should have tier"

    def has_permission(self, request, view):
        return request.user.imgstore_tier is not None
