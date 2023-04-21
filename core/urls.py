from django.urls import path

from core import views
from rest_framework.routers import DefaultRouter

app_name = 'core'

urlpatterns = [
    path('courses/save_teachbase_course/<int:course_id>/', views.SaveTeachbaseCourse.as_view(),
         name='save_teachbase_course')
]

router = DefaultRouter()
router.register('courses', views.CourseViewSet, basename='course')

urlpatterns += router.urls
