# Generated by Django 5.0 on 2024-02-04 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, upload_to='auth_user/', verbose_name='фото'),
        ),
    ]