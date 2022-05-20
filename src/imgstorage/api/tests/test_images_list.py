import pytest

from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework.response import Response

from accounts.models import User


IMAGES_LIST_URL = reverse("images-list")


@pytest.mark.django_db
def test_valid(api: APIClient, authorize, user_basic_account: User, basic_user_image):
    authorize(api, user_basic_account)
    r: Response = api.get(IMAGES_LIST_URL)

    assert r.status_code == 200, r.data
    assert set(r.data.keys()) == {"count", "next", "previous", "results"}
    assert len(r.data["results"]) == 1


@pytest.mark.django_db
def test_valid_empty(api: APIClient, authorize, user_basic_account: User):
    authorize(api, user_basic_account)
    r: Response = api.get(IMAGES_LIST_URL)

    assert r.status_code == 200, r.data
    assert set(r.data.keys()) == {"count", "next", "previous", "results"}
    assert len(r.data["results"]) == 0


@pytest.mark.django_db
def test_invalid_forbidden(api: APIClient, authorize, user: User):
    r: Response = api.get(IMAGES_LIST_URL)

    assert r.status_code == 401, r.data
    assert r.data == {"detail": "Authentication credentials were not provided."}
