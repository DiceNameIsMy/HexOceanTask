import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField

from django.contrib.auth import get_user_model

from .services.expiring_link import s3_expiring_link_client


User = get_user_model()


def get_thumbnail_upload_path(instance: "OriginalImage", filename: str) -> str:
    file_extension = filename.split(".")[-1]
    return f"imgstore/images/thumbnails/{instance.uuid}.{file_extension}"


def get_upload_path(instance: "OriginalImage", filename: str) -> str:
    file_extension = filename.split(".")[-1]
    return f"imgstore/images/{instance.uuid}.{file_extension}"


class AccountTier(models.Model):
    name = models.CharField(max_length=255)
    resolutions = ArrayField(models.IntegerField(), default=list, size=6)

    # Alternatively, we could use JSON field to
    # add new features without changing the database schema
    allow_lossless_resolution = models.BooleanField()
    allow_expiring_links = models.BooleanField()

    class Meta:
        default_related_name = "img_storage_tiers"

    def __str__(self) -> str:
        return self.name

    def max_resolution(self) -> str:
        if self.allow_lossless_resolution:
            return "lossless"
        elif self.resolutions:
            return f"{max(self.resolutions)}px"
        return "none"


class OriginalImage(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=get_upload_path)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # thumbnails imgstorage.ImageThumbnail

    class Meta:
        default_related_name = "images"
        indexes = [models.Index(fields=["uuid"], name="original_image_uuid_idx")]

    def __str__(self) -> str:
        return str(self.uuid)

    def get_image_path(self) -> str:
        return get_upload_path(self, self.image.name)

    @property
    def image_url(self) -> str:
        return s3_expiring_link_client.create_link(self.get_image_path())


class ImageThumbnail(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=get_thumbnail_upload_path)

    resolution = models.IntegerField()
    original = models.ForeignKey(OriginalImage, on_delete=models.CASCADE)

    class Meta:
        default_related_name = "thumbnails"
        indexes = [models.Index(fields=["uuid"], name="image_thumbnail_uuid_idx")]

    def __str__(self) -> str:
        return str(self.uuid)

    def get_image_path(self) -> str:
        return get_thumbnail_upload_path(self, self.image.name)

    @property
    def image_url(self) -> str:
        return s3_expiring_link_client.create_link(self.get_image_path())
