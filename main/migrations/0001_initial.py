# Generated by Django 5.0.4 on 2024-04-09 19:34

import django.core.validators
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, null=True, upload_to='posts/img/')),
                ('video', models.FileField(blank=True, null=True, upload_to='posts/video/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])),
                ('desc', models.TextField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('username', models.CharField(default='', max_length=50)),
                ('comments', models.TextField()),
                ('likes', models.ManyToManyField(blank=True, related_name='liked_posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
