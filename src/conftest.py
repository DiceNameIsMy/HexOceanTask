from typing import Callable

import pytest

from django.core.files.base import ContentFile

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import User
from imgstorage.models import AccountTier, OriginalImage
from imgstorage.api.serializers import ImageSerializer


@pytest.fixture
def api() -> APIClient:
    return APIClient()


@pytest.fixture
def authorize() -> Callable[[APIClient, User], None]:
    def authorizer(api: APIClient, user: User) -> None:
        api.credentials(HTTP_AUTHORIZATION=f"Bearer {str(AccessToken.for_user(user))}")

    return authorizer


@pytest.fixture
def basic_account_tier() -> AccountTier:
    return AccountTier.objects.create(
        name="Basic",
        resolutions=[200],
        allow_lossless_resolution=False,
        allow_expiring_links=False,
    )


@pytest.fixture
def premium_account_tier() -> AccountTier:
    return AccountTier.objects.create(
        name="Premium",
        resolutions=[200, 400],
        allow_lossless_resolution=True,
        allow_expiring_links=False,
    )


@pytest.fixture
def enterprise_account_tier() -> AccountTier:
    return AccountTier.objects.create(
        name="Enterprise",
        resolutions=[200, 400],
        allow_lossless_resolution=True,
        allow_expiring_links=True,
    )


@pytest.fixture
def user() -> User:
    return User.objects.create_user(
        username="user",
        email="user@gmail.com",
        password="password",
        first_name="User",
        last_name="User",
    )


@pytest.fixture
def user_basic_account(basic_account_tier: AccountTier) -> User:
    return User.objects.create_user(
        username="basic_user",
        email="basic_user@gmail.com",
        imgstore_tier=basic_account_tier,
        password="password",
        first_name="User",
        last_name="User",
    )


@pytest.fixture
def user_premium_account(premium_account_tier: AccountTier) -> User:
    return User.objects.create_user(
        username="premium_user",
        email="premium_user@gmail.com",
        imgstore_tier=premium_account_tier,
        password="password",
        first_name="User",
        last_name="User",
    )


@pytest.fixture
def user_enterprise_account(enterprise_account_tier: AccountTier) -> User:
    return User.objects.create_user(
        username="enterprise_user",
        email="enterprise_user@gmail.com",
        imgstore_tier=enterprise_account_tier,
        password="password",
        first_name="User",
        last_name="User",
    )


@pytest.fixture
def jpeg_image() -> ContentFile:
    return ContentFile(
        name="test.jpeg",
        content=open("imgstorage/tests/assets/image.jpeg", "rb").read(),
    )


@pytest.fixture
def basic_user_image(user_basic_account: User, jpeg_image: ContentFile) -> OriginalImage:
    serialzier = ImageSerializer(
        data={
            "image": jpeg_image,
        },
        context={
            "user": user_basic_account,
        },
    )
    serialzier.is_valid(raise_exception=True)
    return serialzier.save()
