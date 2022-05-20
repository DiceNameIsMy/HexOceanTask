from django.urls import path

from .views import UserImageListCreateView


urlpatterns = [
    path("images/", UserImageListCreateView.as_view(), name="images-list"),
]
