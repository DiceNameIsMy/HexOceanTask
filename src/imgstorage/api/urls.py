from django.urls import path

from .views import UserImageListCreateView, CreateOriginalImageExpiringLink, CreateThumbnailExpiringLink


urlpatterns = [
    path("images/", UserImageListCreateView.as_view(), name="images-list"),
    path("images/<uuid:uuid>/link/", CreateOriginalImageExpiringLink.as_view(), name="image-link"),
    path("thumbnails/<uuid:uuid>/link/", CreateThumbnailExpiringLink.as_view(), name="thumbnail-link"),
]
