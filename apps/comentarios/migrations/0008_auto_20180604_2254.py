# Generated by Django 2.0.5 on 2018-06-05 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comentarios', '0007_auto_20180604_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
