# Generated by Django 2.0.5 on 2018-12-31 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0012_auto_20181231_1335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hitcount_articulos',
            name='expired',
        ),
        migrations.AddField(
            model_name='hitcount_articulos',
            name='expired_day',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='hitcount_articulos',
            name='expired_month',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='hitcount_articulos',
            name='expired_week',
            field=models.DateTimeField(null=True),
        ),
    ]