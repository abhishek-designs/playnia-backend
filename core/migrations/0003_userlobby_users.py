# Generated by Django 4.0.2 on 2022-03-02 08:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_userlobby_delete_lobby'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlobby',
            name='users',
            field=models.ManyToManyField(related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]