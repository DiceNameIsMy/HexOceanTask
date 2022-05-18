from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path("accounts/", include("accounts.api.urls")),
    path("admin/", admin.site.urls),
    path(
        "docs/",
        include(
            [
                path("schema/", SpectacularAPIView.as_view(), name="schema"),
                path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),
                path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
            ]
        ),
    ),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # type: ignore
