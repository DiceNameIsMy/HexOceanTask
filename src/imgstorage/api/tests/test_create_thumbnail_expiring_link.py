import pytest

from django.urls import reverse

from rest_framework.test import APIClient

from accounts.models import User
from imgstorage.models import ImageThumbnail


@pytest.mark.django_db
def test_create_link(
    api: APIClient, authorize, user_enterprise_account: User, enterprise_user_200_thumbnail: ImageThumbnail
):
    img = enterprise_user_200_thumbnail
    url = reverse("thumbnail-link", kwargs={"uuid": img.uuid})
    authorize(api, user_enterprise_account)
    r = api.post(url, {"expiration": 300})

    assert r.status_code == 201
    assert r.data == {"expiration": 300, "url": f"http://localhost:8000{img.image.url}"}


@pytest.mark.django_db
def test_too_low_expiration(
    api: APIClient, authorize, user_enterprise_account: User, enterprise_user_200_thumbnail: ImageThumbnail
):
    img = enterprise_user_200_thumbnail
    url = reverse("thumbnail-link", kwargs={"uuid": img.uuid})
    authorize(api, user_enterprise_account)
    r = api.post(url, {"expiration": 299})

    assert r.status_code == 400
    assert r.data == {"expiration": ["Ensure this value is greater than or equal to 300."]}


@pytest.mark.django_db
def test_too_high_expiration(
    api: APIClient, authorize, user_enterprise_account: User, enterprise_user_200_thumbnail: ImageThumbnail
):
    img = enterprise_user_200_thumbnail
    url = reverse("thumbnail-link", kwargs={"uuid": img.uuid})
    authorize(api, user_enterprise_account)
    r = api.post(url, {"expiration": 3001})

    assert r.status_code == 400
    assert r.data == {"expiration": ["Ensure this value is less than or equal to 3000."]}


@pytest.mark.django_db
def test_cant_create_link(
    api: APIClient, authorize, user_premium_account: User, premium_user_200_thumbnail: ImageThumbnail
):
    img = premium_user_200_thumbnail
    url = reverse("thumbnail-link", kwargs={"uuid": img.uuid})
    authorize(api, user_premium_account)
    r = api.post(url, {"expiration": 300})

    assert r.status_code == 403
    assert r.data == {"detail": "Insuffucent account tier."}


@pytest.mark.django_db
def test_does_not_own_image(
    api: APIClient, authorize, user_enterprise_account: User, basic_user_thumbnail: ImageThumbnail
):
    img = basic_user_thumbnail
    url = reverse("thumbnail-link", kwargs={"uuid": img.uuid})
    authorize(api, user_enterprise_account)
    r = api.post(url, {"expiration": 300})

    assert r.status_code == 404
    assert r.data == {"detail": "Not found."}
