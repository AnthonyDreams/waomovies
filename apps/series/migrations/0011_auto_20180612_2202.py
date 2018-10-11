# Generated by Django 2.0.5 on 2018-06-13 02:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('series', '0010_auto_20180527_2102'),
    ]

    operations = [
        migrations.CreateModel(
            name='Votacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('votacion', models.DecimalField(blank=True, choices=[(1, 'uno'), (1.5, 'uno_y_medio'), (2, 'dos'), (2.5, 'dos_y_medio'), (3, 'tres'), (3.5, 'tres_y_medio'), (4, 'cuatro'), (4.5, 'cuatro_y_medio'), (5, 'cinco')], decimal_places=1, max_digits=5, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='capitulos',
            name='serie',
        ),
        migrations.AddField(
            model_name='series',
            name='favoritos',
            field=models.ManyToManyField(blank=True, related_name='favoritos_series', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='series',
            name='palabra_clave',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='series',
            name='portada',
            field=models.ImageField(blank=True, upload_to='static'),
        ),
        migrations.AddField(
            model_name='series',
            name='reportes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='series',
            name='tema',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='series',
            name='ver_mas_tarde',
            field=models.ManyToManyField(blank=True, related_name='ver_mas_tarde_series', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='temporada',
            name='serie',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='series.Series'),
        ),
        migrations.AlterField(
            model_name='series',
            name='genero',
            field=models.CharField(choices=[('ACC', 'Acción'), ('DRA', 'Drama'), ('SC', 'Ciencia_Ficción'), ('TER', 'Terror'), ('SUS', 'Suspenso'), ('CRI', 'Crimen'), ('AVEN', 'Aventura'), ('ANI', 'Animación'), ('COME', 'Comedia')], default='ACC', max_length=20),
        ),
        migrations.AddField(
            model_name='votacion',
            name='pelicula',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='series.Series'),
        ),
        migrations.AddField(
            model_name='votacion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_votacion_serie', to=settings.AUTH_USER_MODEL),
        ),
    ]
