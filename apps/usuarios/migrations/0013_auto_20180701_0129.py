# Generated by Django 2.0.5 on 2018-07-01 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0012_auto_20180627_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='fav_peliculas',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='fav_series',
            field=models.BooleanField(default=False),
        ),
    ]
