# Generated by Django 2.0.5 on 2018-12-01 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notificaciones', '0012_auto_20181201_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificaciones',
            name='komentario',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='komentario', to='comentarios.Post'),
        ),
    ]