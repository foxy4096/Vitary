# Generated by Django 3.2.9 on 2021-12-18 10:15

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0002_auto_20211218_1543'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ChatMessages',
            new_name='ChatMessage',
        ),
    ]
