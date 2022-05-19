import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField

from django.contrib.auth import get_user_model


User = get_user_model()


def get_thumbnail_upload_path(instance: "Image", filename: str) -> str:
    file_extension = filename.split(".")[-1]
    return f"imgstore/images/thumbnails/{instance.uuid}.{file_extension}"


def get_upload_path(instance: "Image", filename: str) -> str:
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
        return self.resolutions.order_by("-resolution")[0]


class Image(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=get_upload_path)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    tier = models.ForeignKey(AccountTier, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        default_related_name = "images"

    def __str__(self) -> str:
        return self.uuid


class ImageThumbnail(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=get_thumbnail_upload_path)

    resolution = models.IntegerField()
    original = models.ForeignKey("Image", on_delete=models.CASCADE)

    class Meta:
        default_related_name = "thumbnails"

    def __str__(self) -> str:
        return self.uuid
