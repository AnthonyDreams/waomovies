# Generated by Django 2.0.5 on 2018-06-14 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0027_auto_20180614_1403'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='votacion',
            name='fecha',
        ),
        migrations.AddField(
            model_name='series',
            name='fecha',
            field=models.ManyToManyField(blank=True, to='series.Vermastarde'),
        ),
    ]
