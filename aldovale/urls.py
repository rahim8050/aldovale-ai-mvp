from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.http import JsonResponse, HttpRequest, HttpResponse


def root_view(request: HttpRequest) -> HttpResponse:
    """Root health/info endpoint."""
    return JsonResponse(
        {
            "message": "Aldovale AI Backend is running.",
            "docs": "/api/v1/docs/redoc/",
            "schema": "/api/v1/docs/swagger/",
        }
    )


urlpatterns = [
    path("", root_view, name="root"),
    path("api/v1/", include("apps.chat.urls")),
    path("api/v1/", include("apps.core.urls")),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/v1/docs/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/v1/docs/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
