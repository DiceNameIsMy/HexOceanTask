from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, AnonymousUser as DjangoAnonymousUser


class User(AbstractUser):
    imgstore_tier = models.ForeignKey(
        "imgstorage.AccountTier", on_delete=models.SET_NULL, null=True, blank=True
    )

    # images imgstorage.OriginalImage

    objects: UserManager


class AnonymousUser(DjangoAnonymousUser):
    pass
