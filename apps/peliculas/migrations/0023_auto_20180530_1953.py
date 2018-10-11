# Generated by Django 2.0.5 on 2018-05-30 23:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('peliculas', '0022_auto_20180530_1920'),
    ]

    operations = [
        migrations.AddField(
            model_name='personajes',
            name='actor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='peliculas.Cast'),
        ),
        migrations.AlterField(
            model_name='personajes',
            name='pelicula',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='peliculas.Peliculas'),
        ),
    ]
