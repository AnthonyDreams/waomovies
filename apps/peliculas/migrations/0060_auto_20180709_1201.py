# Generated by Django 2.0.5 on 2018-07-09 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peliculas', '0059_auto_20180709_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cast',
            name='picture',
            field=models.ImageField(null=True, upload_to='static'),
        ),
    ]
