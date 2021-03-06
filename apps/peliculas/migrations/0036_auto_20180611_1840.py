# Generated by Django 2.0.5 on 2018-06-11 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peliculas', '0035_peliculas_view_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peliculas',
            name='genero',
            field=models.CharField(choices=[('ACC', 'Acción'), ('DRA', 'Drama'), ('SC', 'Ciencia_Ficción'), ('TER', 'Terror'), ('SUS', 'Suspenso'), ('CRI', 'Crimen'), ('AVEN', 'Aventura'), ('ANI', 'Animación'), ('COME', 'Comedia')], max_length=20),
        ),
        migrations.AlterField(
            model_name='peliculas',
            name='view_time',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
