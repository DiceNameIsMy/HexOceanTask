from django.contrib import admin

from .models import AccountTier, ImageThumbnail, OriginalImage


@admin.register(ImageThumbnail)
class ImageThumbnailAdmin(admin.ModelAdmin):
    list_display = ["uuid", "image", "resolution", "original"]
    list_filter = ["resolution"]


@admin.register(OriginalImage)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("user", "uuid", "image")
    list_filter = ("user",)


@admin.register(AccountTier)
class AccountTierAdmin(admin.ModelAdmin):
    list_display = ("name", "allow_lossless_resolution", "allow_expiring_links", "max_resolution")
    search_fields = ("name",)
    list_filter = ("resolutions", "allow_lossless_resolution", "allow_expiring_links")
