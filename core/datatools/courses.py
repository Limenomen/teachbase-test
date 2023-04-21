from lib.teachbase import TeachbaseClient
from core import serializers


def save_teachbase_course(course_id: int):
    course_data = TeachbaseClient().get_course(course_id=course_id)
    course_serializer = serializers.Course(data=course_data)
    course_serializer.is_valid(raise_exception=True)
    return course_serializer.save()
