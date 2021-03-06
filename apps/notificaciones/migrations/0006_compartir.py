# Generated by Django 2.0.5 on 2018-11-27 03:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('series', '0051_auto_20180705_1542'),
        ('peliculas', '0063_auto_20180709_2256'),
        ('notificaciones', '0005_auto_20181124_1450'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compartir',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.CharField(blank=True, max_length=150, null=True)),
                ('capitulo_to_share', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='series.Capitulos')),
                ('movie_to_share', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='peliculas.Peliculas')),
                ('serie_to_share', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='series.Series')),
                ('user_to_share', models.ManyToManyField(related_name='user_to_share', to=settings.AUTH_USER_MODEL)),
                ('user_who_share', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
