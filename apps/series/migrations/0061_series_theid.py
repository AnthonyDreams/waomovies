# Generated by Django 2.0.5 on 2019-04-15 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0060_auto_20190326_1904'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='theid',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]
