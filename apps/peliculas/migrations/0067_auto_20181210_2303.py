# Generated by Django 2.0.5 on 2018-12-11 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peliculas', '0066_hitcount_hitcount_ever'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hitcount',
            name='expired',
            field=models.DateTimeField(),
        ),
    ]
