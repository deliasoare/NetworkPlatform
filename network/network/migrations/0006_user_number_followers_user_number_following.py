# Generated by Django 4.1.2 on 2022-12-29 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_alter_post_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='number_followers',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='number_following',
            field=models.IntegerField(default=0),
        ),
    ]
