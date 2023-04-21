from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from core import models
from rest_framework.permissions import IsAuthenticated
from core import datatools, serializers


class CourseViewSet(ReadOnlyModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = serializers.Course
    permission_classes = (IsAuthenticated,)


class SaveTeachbaseCourse(APIView):
    """Сохранение курса из Teachbase"""
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request, course_id: int) -> Response:
        teachbase_course = datatools.courses.save_teachbase_course(course_id=course_id)
        return Response(serializers.Course(instance=teachbase_course).data)


