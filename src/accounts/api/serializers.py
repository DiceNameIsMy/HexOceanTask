from rest_framework import serializers

from accounts.models import User


class UserDetailSerialzier(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "is_superuser",
            "date_joined",
        )
