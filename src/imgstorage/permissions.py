from rest_framework.permissions import BasePermission


class HasAccountTier(BasePermission):
    message = "User should have tier."

    def has_permission(self, request, view):
        return request.user.imgstore_tier is not None


class CanAccessOriginalImage(BasePermission):
    message = "Insuffucent account tier."

    def has_permission(self, request, view):
        return request.user.imgstore_tier.allow_lossless_resolution


class CanCreateExpiringLink(BasePermission):
    message = "Insuffucent account tier."

    def has_permission(self, request, view):
        return request.user.imgstore_tier.allow_expiring_links
