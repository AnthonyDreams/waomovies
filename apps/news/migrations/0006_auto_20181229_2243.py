# Generated by Django 2.0.5 on 2018-12-30 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_auto_20181229_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='media',
            field=models.ManyToManyField(blank=True, null=True, related_name='media', to='news.NewsMedia'),
        ),
    ]