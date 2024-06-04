from django.db import models
from django.contrib.auth.models import AbstractUser

class SubscriptionModel(models.Model):

    user_from = models.ForeignKey('auth_user.Profile', related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth_user.Profile', related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created'])
        ]
        ordering = ['-created']

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


class Profile(AbstractUser):
    photo = models.ImageField(blank=True, upload_to='auth_user/', verbose_name='фото')
    following = models.ManyToManyField('self', through=SubscriptionModel, related_name='followers', symmetrical=False)
