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
        ordering = ['-date_create']
        indexes = [
            models.Index(fields=['-date_create'])
            ]
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
    

class CommentsModel(models.Model):

    body = models.TextField()
    date_create = models.DateField(auto_now_add=True, verbose_name='Время создания')
    date_update =  models.DateField(auto_now=True, verbose_name='Время изменения')
    active = models.BooleanField(default=True)
    user = models.ForeignKey('auth_user.Profile', on_delete=models.CASCADE, related_name='nickname', verbose_name='Автор')
    post = models.ForeignKey(PostsModel, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ['-date_create']
        indexes = [
            models.Index(fields=['-date_create'])
            ]
        verbose_name = 'Комментарии Пользователей'
        verbose_name_plural = 'Комментарии Пользователей'

    def __str__(self):
        return f'Комментарий пользвателя {self.user.username} к посту {self.post.title}'