from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Action(models.Model):

    user = models.ForeignKey('auth_user.Profile', related_name='actions', on_delete=models.CASCADE, verbose_name='Пользователь')
    verb = models.CharField(max_length=255, verbose_name='Действие пользователя')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    target_ct = models.ForeignKey(ContentType, blank=True, null=True, related_name='target_obj', on_delete=models.CASCADE, verbose_name='Указатель на модель')
    target_id = models.PositiveIntegerField(null=True, blank=True, verbose_name='pk')
    target = GenericForeignKey('target_ct', 'target_id')
 
    class Meta:
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['target_ct', 'target_id'])
        ]
        ordering = ['-created']
        verbose_name = 'Действие пользователя'
        verbose_name_plural = 'Действия пользователей'
