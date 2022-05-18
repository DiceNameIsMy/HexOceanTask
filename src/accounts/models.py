from django.contrib.auth.models import AbstractUser, UserManager, AnonymousUser as DjangoAnonymousUser


class User(AbstractUser):
    objects: UserManager


class AnonymousUser(DjangoAnonymousUser):
    pass
