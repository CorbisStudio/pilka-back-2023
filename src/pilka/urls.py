from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions

# OpenAPI import
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# SimpleJWT import
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

api_patterns = ([
    path('', include('api.users.urls')),
])

doc_patterns = ([
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
            cache_timeout=0), name='schema-redoc'),
])

token_pattern = ([
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
])

urlpatterns = [
    path('', include(doc_patterns)),
    path('', include(token_pattern)),
    path('v1/', include(api_patterns)),
    path('admin/', admin.site.urls),
]
