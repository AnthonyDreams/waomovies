# Generated by Django 2.0.5 on 2018-06-09 02:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peliculas', '0032_peliculas_ver_mas_tarde'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peliculas',
            name='ver_mas_tarde',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
