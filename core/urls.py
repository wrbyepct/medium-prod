"""Project level urls."""

from dj_rest_auth.views import PasswordResetConfirmView
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from core.apps.user.views import CustomUserDetailsView

admin.site.site_header = "Medium API Admin"
admin.site.site_title = "Medium API Admin Portal"
admin.site.index_title = "Welcome to Medium API Admin"

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/v1/auth/user/me/", CustomUserDetailsView.as_view(), name="user_details"),
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    path("api/v1/auth/registration/", include("dj_rest_auth.registration.urls")),
    path(
        "api/v1/auth/password_rest/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("api/v1/profiles/", include("core.apps.profiles.urls")),
    path("api/v1/articles/", include("core.apps.articles.urls")),
    path("api/v1/ratings/", include("core.apps.ratings.urls")),
    path("api/v1/bookmarks/", include("core.apps.bookmarks.urls")),
    path("api/v1/responses/", include("core.apps.responses.urls")),
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

if settings.DEBUG and not settings.IN_TEST:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns = urlpatterns + debug_toolbar_urls()
