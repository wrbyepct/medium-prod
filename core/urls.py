from django.conf import settings
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

admin.site.site_header = "Medium API Admin"
admin.site.site_title = "Medium API Admin Portal"
admin.site.index_title = "Welcome to Medium API Admin"

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
]


urlpatterns += [
    # Your API endpoints
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
