# Generated by Django 2.0.5 on 2018-05-29 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peliculas', '0008_auto_20180529_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='label',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
