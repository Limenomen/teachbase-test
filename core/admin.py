from django.contrib import admin
from core import models


@admin.register(models.Course)
class Course(admin.ModelAdmin):
    list_display = ('name', 'owner_name', 'created_at')

