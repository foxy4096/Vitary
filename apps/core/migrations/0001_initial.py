# Generated by Django 4.0.2 on 2022-03-02 03:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('color', models.CharField(choices=[('success', 'Green'), ('info', 'Blue'), ('link', 'Purple'), ('primary', 'Turquoise'), ('warning', 'Yellow'), ('danger', 'Red'), ('dark', 'Black'), ('white', 'White')], max_length=50)),
                ('special', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Requirments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('badge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.badge')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Abuse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abuse_type', models.CharField(choices=[('ABUSE', 'Abuse'), ('INAPPROPRIATE', 'Inappropriate'), ('SPAM', 'Spam'), ('BULLYING', 'Bullying'), ('SEXUAL_CONTENT', 'Sexual Content'), ('OTHER', 'Other')], max_length=50)),
                ('description', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('to_vit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vit.vit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Abuses',
                'ordering': ['-date'],
            },
        ),
    ]
