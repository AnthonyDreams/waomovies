# Generated by Django 2.0.5 on 2018-12-29 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='publish',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='article',
            name='slug',
            field=models.CharField(default=23156478, max_length=8, unique=True),
            preserve_default=False,
        ),
    ]
