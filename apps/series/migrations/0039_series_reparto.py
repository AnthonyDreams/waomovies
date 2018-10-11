# Generated by Django 2.0.5 on 2018-07-01 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peliculas', '0049_peliculas_genero2'),
        ('series', '0038_series_genero2'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='reparto',
            field=models.ManyToManyField(blank=True, related_name='reparto_serie', to='peliculas.Cast'),
        ),
    ]
