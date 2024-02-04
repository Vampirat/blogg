from django.db import models
from django.urls import reverse


from pytils.translit import slugify




class PostsModel(models.Model):
    
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    text = models.TextField(max_length=500, verbose_name='Пост')
    slug = models.SlugField(unique=True, verbose_name='slug')
    date_create = models.DateField(auto_now_add=True, verbose_name='Время создания')
    date_update =  models.DateField(auto_now=True, verbose_name='Время изменения')
    picture = models.ImageField(upload_to='photos/posts', blank=True, default=None, verbose_name='Фото')
    is_published = models.BooleanField(default=True, verbose_name='Отображение поста в общей ленте')
    user = models.ForeignKey('auth_user.Profile', on_delete=models.CASCADE, related_name='author', verbose_name='Автор')

    class Meta:

        verbose_name = 'Посты пользователей'
        verbose_name_plural = 'Посты пользователей'


    def save(self, *args, **kwargs):

        self.slug = slugify(self.title)
        try:
            return super().save(*args, **kwargs)
        except:
            uniq_slug = slugify(self.title) + '-' + slugify(str(self.date_create))    #позже вместо  времени взять никнейм
            self.slug = slugify(uniq_slug)
            return super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('selected_post', kwargs={'slug': self.slug})