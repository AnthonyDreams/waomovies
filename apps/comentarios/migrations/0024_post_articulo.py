# Generated by Django 2.0.5 on 2018-12-31 19:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0013_auto_20181231_1402'),
        ('comentarios', '0023_auto_20180629_0159'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='articulo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='news.Article'),
        ),
    ]