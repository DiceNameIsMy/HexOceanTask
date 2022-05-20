from io import BytesIO

from PIL import Image

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction

from rest_framework import serializers

from imgstorage.models import AccountTier, OriginalImage, ImageThumbnail


class CurrentUserDefault:
    requires_context = True

    def __call__(self, serializer_field: serializers.Serializer) -> AccountTier | None:
        try:
            return serializer_field.context["request"].user
        except (KeyError, AttributeError):
            # used in tests to not provide `Request` to context
            return serializer_field.context.get("user", None)

    def __repr__(self):
        return "%s()" % self.__class__.__name__


class ImageThumbnailSerialzier(serializers.ModelSerializer):
    class Meta:
        model = ImageThumbnail
        fields = ("uuid", "image", "resolution")


class AccountTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountTier
        fields = (
            "name",
            "resolutions",
            "allow_lossless_resolution",
            "allow_expiring_links",
        )


class ImageSerializer(serializers.ModelSerializer):
    thumbnails = ImageThumbnailSerialzier(many=True, read_only=True)
    user = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = OriginalImage
        fields = ("id", "uuid", "image", "user", "thumbnails")

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if not self.context["request"].user.imgstore_tier.allow_lossless_resolution:
            ret.pop("uuid")
            ret.pop("image")

        return ret

    @transaction.atomic
    def create(self, validated_data):
        image: InMemoryUploadedFile = validated_data["image"]
        pil_image: Image.Image = Image.open(image).copy()
        original_width, _ = pil_image.size
        resolutions: list[int] = sorted(validated_data["user"].imgstore_tier.resolutions, reverse=True)
        original_image: OriginalImage = super().create(validated_data)

        image_thumbnails: list[ImageThumbnail] = []
        for res in resolutions:
            io = BytesIO()
            pil_image.thumbnail((original_width, res))
            pil_image.save(io, format=image.content_type.split("/")[-1])
            image_thumbnails.append(
                ImageThumbnail(
                    image=ContentFile(content=io.getvalue(), name=image.name),
                    resolution=res,
                    original=original_image,
                )
            )

        ImageThumbnail.objects.bulk_create(image_thumbnails)
        return original_image
