# Generated by Django 2.0.5 on 2018-06-14 21:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peliculas', '0039_peliculas_fecha'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='peliculas',
            name='fecha',
        ),
        migrations.RemoveField(
            model_name='peliculas',
            name='ver_mas_tarde',
        ),
    ]
