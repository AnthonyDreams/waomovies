# Generated by Django 2.0.5 on 2018-05-30 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peliculas', '0017_auto_20180530_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trailers',
            name='reparto',
            field=models.ManyToManyField(blank=True, to='peliculas.Cast'),
        ),
    ]
