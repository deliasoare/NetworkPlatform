# Generated by Django 4.1.2 on 2022-12-30 14:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0011_remove_user_followerss_remove_user_following_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(null=True, related_name='Followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(null=True, related_name='Following', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Follow',
        ),
    ]