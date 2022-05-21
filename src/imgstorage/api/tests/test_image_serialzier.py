import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.fields.files import ImageFieldFile
from django.core.files.base import ContentFile

from accounts.models import User
from imgstorage.models import OriginalImage
from imgstorage.api.serializers import ImageSerializer


@pytest.mark.django_db
def test_create_image(user_basic_account: User, jpeg_image: ContentFile):
    serialzier = ImageSerializer(
        data={
            "image": SimpleUploadedFile(
                name="test.jpeg",
                content=jpeg_image.read(),
                content_type="image/jpeg",
            ),
        },
        context={
            "user": user_basic_account,
        },
    )
    serialzier.is_valid(raise_exception=True)
    image_model: OriginalImage = serialzier.save()
    image: ImageFieldFile = image_model.image
    thumbnails = image_model.thumbnails.all()
    assert image_model.user == user_basic_account

    assert image.height == 667
    assert image.width == 1000

    assert thumbnails.count() == len(user_basic_account.imgstore_tier.resolutions)

    for t in thumbnails:
        assert t.image.width <= image.width
        assert t.image.height <= t.resolution
