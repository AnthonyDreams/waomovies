# Generated by Django 2.0.5 on 2018-07-03 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peliculas', '0052_auto_20180702_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cast',
            name='personaje_fname',
            field=models.ManyToManyField(blank=True, related_name='actor', to='peliculas.Personajes'),
        ),
    ]
