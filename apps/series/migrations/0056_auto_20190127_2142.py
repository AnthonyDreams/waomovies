# Generated by Django 2.0.5 on 2019-01-28 01:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('series', '0055_auto_20190127_2136'),
    ]

    operations = [
        migrations.CreateModel(
            name='Busqueda_y_etiquetas_series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(blank=True, max_length=80, null=True)),
                ('timestamp_tag', models.DateTimeField(auto_now_add=True)),
                ('resuelto', models.BooleanField(default=False)),
                ('user_who_search', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='series',
            name='otras_etiquetas_y_busquedas',
            field=models.ManyToManyField(blank=True, related_name='otras_etiquetas_y_busquedas', to='series.Busqueda_y_etiquetas_series'),
        ),
    ]
