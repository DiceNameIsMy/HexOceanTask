from typing import Callable

import pytest

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import User


@pytest.fixture
def api() -> APIClient:
    return APIClient()


@pytest.fixture
def authorize() -> Callable[[APIClient, User], None]:
    def authorizer(api: APIClient, user: User) -> None:
        api.credentials(HTTP_AUTHORIZATION=f"Bearer {str(AccessToken.for_user(user))}")

    return authorizer


@pytest.fixture
def user() -> User:
    return User.objects.create_user(
        username="user",
        email="user@gmail.com",
        password="password",
        first_name="User",
        last_name="User",
    )
