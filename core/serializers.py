from rest_framework import serializers
from core import models


class Course(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = '__all__'
