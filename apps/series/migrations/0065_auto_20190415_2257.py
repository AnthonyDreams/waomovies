# Generated by Django 2.0.5 on 2019-04-16 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0064_auto_20190415_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='fecha_de_lanzamiento',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='series',
            name='sinopsis',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='series',
            name='titulo',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='series',
            name='titulo_original',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
