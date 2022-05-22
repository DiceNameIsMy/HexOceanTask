from io import BytesIO

from PIL import Image
from django.conf import settings

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile

from rest_framework import serializers

from imgstorage.models import OriginalImage, ImageThumbnail
from imgstorage.services.expiring_link import s3_expiring_link_client


class GetFromSerializerContext(serializers.CurrentUserDefault):
    def __init__(self, field: str) -> None:
        self.field = field

    def __call__(self, serializer_field: serializers.Serializer):
        return serializer_field.context[self.field]


class ImageThumbnailSerialzier(serializers.ModelSerializer):
    class Meta:
        model = ImageThumbnail
        fields = ("uuid", "image", "resolution")


class ImageSerializer(serializers.ModelSerializer):
    thumbnails = ImageThumbnailSerialzier(many=True, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = OriginalImage
        fields = ("id", "uuid", "image", "user", "thumbnails")

    def validate_image(self, image: InMemoryUploadedFile) -> InMemoryUploadedFile:
        if image.name.split(".")[-1] not in settings.ALLOWED_IMAGE_FORMATS:
            raise serializers.ValidationError(f"`{image.name}` does not have allowed file extensions.")
        return image

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if not self.context["request"].user.imgstore_tier.allow_lossless_resolution:
            ret.pop("uuid")
            ret.pop("image")

        return ret

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


class ExpiringLinkSerializer(serializers.Serializer):
    # provide `model` to Meta class after inheriting from this class

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    image = serializers.HiddenField(default=GetFromSerializerContext("object"))
    expiration = serializers.IntegerField(
        min_value=settings.IMAGE_LINK_MIN_EXPIRATION, max_value=settings.IMAGE_LINK_MAX_EXPIRATION
    )
    url = serializers.URLField(read_only=True)

    def __init__(self, *args, **kwargs):
        assert hasattr(self, "Meta"), "You must provide `Meta` class"
        assert hasattr(self.Meta, "model"), "You must provide `model` to Meta class"
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        validated_data["url"] = s3_expiring_link_client.create_link(
            url=validated_data["image"].get_image_path(),
            exp=validated_data["expiration"],
        )
        return validated_data


class ImageExpiringLinkSerializer(ExpiringLinkSerializer):
    class Meta:
        model = OriginalImage


class ThumbnailExpiringLinkSerializer(ExpiringLinkSerializer):
    class Meta:
        model = ImageThumbnail
