from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.conf import settings
import os

schema_view = get_schema_view(
    openapi.Info(
        title='Teachbase test',
        default_version='v1',
        description='Teachbase test',
    )
)

urlpatterns = [
    path('', include('core.urls', namespace='core')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
]
