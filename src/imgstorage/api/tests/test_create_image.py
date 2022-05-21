import pytest

from django.urls import reverse

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import ContentFile

from rest_framework.test import APIClient
from rest_framework.response import Response

from accounts.models import User


IMAGES_LIST_URL = reverse("images-list")


@pytest.mark.django_db
def test_create_valid_basic(api: APIClient, authorize, user_basic_account: User, jpeg_image: ContentFile):
    authorize(api, user_basic_account)
    data = {
        "image": SimpleUploadedFile(
            "test.jpeg", jpeg_image.read(), content_type="image/jpeg"
        ),
    }
    r: Response = api.post(IMAGES_LIST_URL, data)

    assert r.status_code == 201, r.data
    assert set(r.data.keys()) == {"id", "thumbnails"}
    assert len(r.data["thumbnails"]) == 1


@pytest.mark.django_db
def test_create_valid_premium(api: APIClient, authorize, user_premium_account: User, jpeg_image: ContentFile):
    authorize(api, user_premium_account)
    data = {
        "image": SimpleUploadedFile(
            "test.jpeg", jpeg_image.read(), content_type="image/jpeg"
        ),
    }
    r: Response = api.post(IMAGES_LIST_URL, data)

    assert r.status_code == 201, r.data
    assert set(r.data.keys()) == {"id", "uuid", "image", "thumbnails"}
    assert len(r.data["thumbnails"]) == 2


@pytest.mark.django_db
def test_create_valid_enterprise(api: APIClient, authorize, user_enterprise_account: User, jpeg_image: ContentFile):
    authorize(api, user_enterprise_account)
    data = {
        "image": SimpleUploadedFile(
            "test.jpeg", jpeg_image.read(), content_type="image/jpeg"
        ),
    }
    r: Response = api.post(IMAGES_LIST_URL, data)

    assert r.status_code == 201, r.data
    assert set(r.data.keys()) == {"id", "uuid", "image", "thumbnails"}
    assert len(r.data["thumbnails"]) == 2


@pytest.mark.django_db
def test_unauthorized(api: APIClient, authorize, user_basic_account: User, jpeg_image: ContentFile):
    data = {
        "image": SimpleUploadedFile(
            "test.jpeg", jpeg_image.read(), content_type="image/jpeg"
        ),
    }
    r: Response = api.post(IMAGES_LIST_URL, data)

    assert r.status_code == 401, r.data
    assert r.data == {"detail": "Authentication credentials were not provided."}
