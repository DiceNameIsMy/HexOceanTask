from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from imgstorage.models import OriginalImage
from imgstorage.permissions import HasAccountTier

from .serializers import ImageSerializer


class UserImageListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, HasAccountTier)
    serializer_class = ImageSerializer

    def get_queryset(self):
        return (
            OriginalImage.objects.filter(user=self.request.user).prefetch_related("thumbnails")
        )
