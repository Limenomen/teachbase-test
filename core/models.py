from django.db import models


class Course(models.Model):
    name = models.CharField('название', max_length=255)
    created_at = models.DateTimeField('дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('дата последнего обновления', auto_now=True)
    description = models.TextField('описание')
    demo = models.BooleanField('демо-версия', default=False)
    owner_id = models.IntegerField('id владельца')
    owner_name = models.CharField('имя владельца', max_length=255)

    def __str__(self):
        return f'курс: "{self.name}", владелец: {self.owner_name}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


