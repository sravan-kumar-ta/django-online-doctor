from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_ui

schema_view = swagger_ui(
   openapi.Info(
      title="Online Doctor API",
      default_version='v1.0.0',
      description="Test description",
   ),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('account/', include("accounts.urls")),
    path('doctor/', include("doctors.urls")),
    path('blogs/', include('blogs.urls')),
    path('chat/', include('chat.urls')),
    path('api/', include("api.urls")),
    path('', include("patients.urls")),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
