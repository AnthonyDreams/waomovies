# Generated by Django 2.0.5 on 2018-05-25 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peliculas', '0004_auto_20180521_2100'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='peliculas',
            options={'verbose_name_plural': 'Películas'},
        ),
        migrations.AddField(
            model_name='peliculas',
            name='links',
            field=models.TextField(blank=True, null=True),
        ),
    ]
