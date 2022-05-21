from PIL import Image

import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.fields.files import ImageFieldFile
from django.core.files.base import ContentFile

from accounts.models import User
from imgstorage.models import OriginalImage
from imgstorage.api.serializers import ImageSerializer


from conftest import FakeRequest


@pytest.mark.django_db
def test_create_image(user_basic_account: User, png_image: ContentFile):
    png_image_bytes = png_image.read()
    png_image_width, png_image_height = Image.open(png_image).size
    serialzier = ImageSerializer(
        data={
            "image": SimpleUploadedFile(
                name=png_image.name,
                content=png_image_bytes,
                content_type="image/png",
            ),
        },
        context={"request": FakeRequest(user_basic_account)},
    )
    serialzier.is_valid(raise_exception=True)
    image_model: OriginalImage = serialzier.save()
    image: ImageFieldFile = image_model.image
    thumbnails = image_model.thumbnails.all()
    assert image_model.user == user_basic_account

    assert image.height == png_image_height
    assert image.width == png_image_width

    assert thumbnails.count() == len(user_basic_account.imgstore_tier.resolutions)

    for t in thumbnails:
        assert t.image.width <= image.width
        assert t.image.height <= t.resolution


@pytest.mark.django_db
def test_image_format(user_basic_account: User, jpeg_image: ContentFile):
    serialzier = ImageSerializer(
        data={
            "image": SimpleUploadedFile(
                name=jpeg_image.name,
                content=jpeg_image.read(),
                content_type="image/jpeg",
            ),
        },
        context={"request": FakeRequest(user_basic_account)},
    )
    assert not serialzier.is_valid()


@pytest.mark.django_db
def test_bad_file(user_basic_account: User, word_document: ContentFile):
    serialzier = ImageSerializer(
        data={
            "image": SimpleUploadedFile(
                name=word_document.name,
                content=word_document.read(),
                content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ),
        },
        context={"request": FakeRequest(user_basic_account)},
    )
    assert not serialzier.is_valid()
