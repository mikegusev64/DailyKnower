# Generated by Django 5.1.2 on 2024-12-30 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0015_notes_notepost'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notes',
            old_name='notePost',
            new_name='relatedAdminPost',
        ),
    ]
