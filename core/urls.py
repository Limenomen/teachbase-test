from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from core import views
from rest_framework.routers import DefaultRouter

schema_view = get_schema_view(
    openapi.Info(
        title='Teachbase test',
        default_version='v1',
        description='Teachbase test',
    )
)

app_name = 'core'

urlpatterns = [
]

router = DefaultRouter()
router.register('courses/', views.CourseViewSet, basename='course')

urlpatterns += router.urls
