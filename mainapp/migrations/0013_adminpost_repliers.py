# Generated by Django 5.1.2 on 2024-12-22 19:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_adminpost_topictheme'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='adminpost',
            name='repliers',
            field=models.ManyToManyField(blank=True, related_name='repliers', to=settings.AUTH_USER_MODEL),
        ),
    ]