# Generated by Django 2.0.5 on 2018-06-17 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peliculas', '0041_auto_20180616_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='peliculas',
            name='tag1',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='peliculas',
            name='tag2',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='peliculas',
            name='tag3',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
