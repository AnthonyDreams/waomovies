# Generated by Django 2.0.5 on 2018-12-08 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0051_auto_20180705_1542'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='series',
            name='openload',
        ),
        migrations.RemoveField(
            model_name='series',
            name='rapidvideo',
        ),
        migrations.RemoveField(
            model_name='series',
            name='streamago',
        ),
        migrations.RemoveField(
            model_name='series',
            name='vidoza',
        ),
        migrations.RemoveField(
            model_name='series',
            name='webtorrent',
        ),
        migrations.AddField(
            model_name='capitulos',
            name='openload',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='capitulos',
            name='rapidvideo',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='capitulos',
            name='servidor1',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='capitulos',
            name='servidor2',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='capitulos',
            name='servidor3',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='capitulos',
            name='servidor4',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='capitulos',
            name='streamago',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='capitulos',
            name='streamcloud',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='capitulos',
            name='vidlox',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='capitulos',
            name='vidoza',
            field=models.TextField(blank=True, null=True),
        ),
    ]
