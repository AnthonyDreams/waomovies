# Generated by Django 2.0.5 on 2018-06-03 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0007_auto_20180602_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='staff',
            field=models.BooleanField(default=False),
        ),
    ]
