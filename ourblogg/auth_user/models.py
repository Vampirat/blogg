from django.db import models
from django.contrib.auth.models import AbstractUser

class Profile(AbstractUser):
    photo = models.ImageField(blank=True, upload_to='auth_user/', verbose_name='фото')