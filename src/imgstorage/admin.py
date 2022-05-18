from django.contrib import admin

from .models import ImageResolution, AccountTier, Image


@admin.register(ImageResolution)
class ImageResolutionAdmin(admin.ModelAdmin):
    list_display = ["resolution"]
    list_filter = ["resolution"]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("user", "image", "resolution")
    list_filter = ("user", "resolution")


@admin.register(AccountTier)
class AccountTierAdmin(admin.ModelAdmin):
    list_display = ("name", "allow_lossless_resolution", "allow_expiring_links", "max_resolution")
    search_fields = ("name",)
    list_filter = ("resolutions", "allow_lossless_resolution", "allow_expiring_links")
