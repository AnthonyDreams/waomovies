# Generated by Django 2.0.5 on 2018-07-02 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0041_hitcount_series'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='reparto',
            field=models.ManyToManyField(blank=True, related_name='reparto_serie', to='peliculas.Personajes'),
        ),
    ]
