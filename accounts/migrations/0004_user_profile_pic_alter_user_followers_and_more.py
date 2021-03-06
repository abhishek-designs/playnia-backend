# Generated by Django 4.0.2 on 2022-03-01 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_followers_user_following_user_total_answers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.FileField(blank=True, upload_to='', verbose_name='profile pic'),
        ),
        migrations.AlterField(
            model_name='user',
            name='followers',
            field=models.IntegerField(blank=True, default=0, verbose_name='followers'),
        ),
        migrations.AlterField(
            model_name='user',
            name='following',
            field=models.IntegerField(blank=True, default=0, verbose_name='following'),
        ),
        migrations.AlterField(
            model_name='user',
            name='total_answers',
            field=models.IntegerField(blank=True, default=0, verbose_name='total answers'),
        ),
        migrations.AlterField(
            model_name='user',
            name='total_questions',
            field=models.IntegerField(blank=True, default=0, verbose_name='total questions'),
        ),
    ]
