from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from imgstorage.models import ImageThumbnail, OriginalImage
from imgstorage.permissions import CanAccessOriginalImage, CanCreateExpiringLink, HasAccountTier

from .serializers import ImageExpiringLinkSerializer, ImageSerializer


class UserImageListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, HasAccountTier)
    serializer_class = ImageSerializer

    def get_queryset(self):
        return OriginalImage.objects.filter(user=self.request.user).prefetch_related("thumbnails")


class CreateOriginalImageExpiringLink(CreateAPIView):
    permission_classes = (IsAuthenticated, HasAccountTier, CanAccessOriginalImage, CanCreateExpiringLink)
    serializer_class = ImageExpiringLinkSerializer
    lookup_field = "uuid"

    def get_queryset(self):
        return OriginalImage.objects.filter(user=self.request.user)

    def get_serializer_context(self) -> dict:
        context = super().get_serializer_context()
        context["object"] = self.get_object()
        return context


class CreateThumbnailExpiringLink(CreateAPIView):
    permission_classes = (IsAuthenticated, HasAccountTier, CanCreateExpiringLink)
    serializer_class = ImageExpiringLinkSerializer
    lookup_field = "uuid"

    def get_queryset(self):
        return ImageThumbnail.objects.filter(original__user=self.request.user)

    def get_serializer_context(self) -> dict:
        context = super().get_serializer_context()
        context["object"] = self.get_object()
        return context
