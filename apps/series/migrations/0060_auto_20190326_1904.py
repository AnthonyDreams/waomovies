# Generated by Django 2.0.5 on 2019-03-26 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0059_auto_20190128_2319'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='CoverImg',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='series',
            name='PortadaImg',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
