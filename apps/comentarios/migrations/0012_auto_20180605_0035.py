# Generated by Django 2.0.5 on 2018-06-05 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comentarios', '0011_auto_20180604_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.IntegerField(default=0, unique=True),
        ),
    ]
