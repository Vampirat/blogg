# Generated by Django 5.0 on 2023-12-21 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PostsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('text', models.TextField(max_length=500, verbose_name='Пост')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('date_create', models.DateField(auto_now_add=True, verbose_name='Время создания')),
                ('date_update', models.DateField(auto_now=True, verbose_name='Время изменения')),
                ('picture', models.ImageField(blank=True, default=None, upload_to='photos/', verbose_name='Фото')),
                ('is_published', models.BooleanField(default=True, verbose_name='Отображение поста в общей ленте')),
            ],
        ),
    ]
