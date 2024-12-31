# Generated by Django 5.1.2 on 2024-12-30 09:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0013_adminpost_repliers'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('noteContent', models.TextField()),
                ('noteTheme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.topictheme')),
                ('noteTopic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.dktopic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
