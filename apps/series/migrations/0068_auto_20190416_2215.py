# Generated by Django 2.0.5 on 2019-04-17 02:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0067_auto_20190416_2151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='capitulos',
            name='director',
        ),
        migrations.RemoveField(
            model_name='capitulos',
            name='nombre_original',
        ),
    ]
