from django.db import models

from django.contrib.auth import get_user_model


User = get_user_model()


class ImageResolution(models.Model):
    resolution = models.PositiveIntegerField(unique=True)

    def __str__(self) -> str:
        return str(self.resolution)


class AccountTier(models.Model):
    name = models.CharField(max_length=255)
    resolutions = models.ManyToManyField(ImageResolution)
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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    tier = models.ForeignKey(AccountTier, on_delete=models.SET_NULL, null=True, blank=True)
    resolution = models.ForeignKey(ImageResolution, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField()

    class Meta:
        default_related_name = "images"

    def __str__(self) -> str:
        return self.image
