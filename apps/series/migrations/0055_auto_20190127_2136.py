# Generated by Django 2.0.5 on 2019-01-28 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0054_auto_20190127_2133'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='tag4',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='series',
            name='tag5',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='series',
            name='tag6',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='series',
            name='tag7',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='series',
            name='tag1',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='series',
            name='tag2',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='series',
            name='tag3',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]