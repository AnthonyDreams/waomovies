# Generated by Django 2.0.5 on 2018-05-28 01:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0009_auto_20180527_2043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='members',
        ),
        migrations.RemoveField(
            model_name='membership',
            name='group',
        ),
        migrations.RemoveField(
            model_name='membership',
            name='inviter',
        ),
        migrations.RemoveField(
            model_name='membership',
            name='person',
        ),
        migrations.DeleteModel(
            name='Group',
        ),
        migrations.DeleteModel(
            name='Membership',
        ),
        migrations.DeleteModel(
            name='Person',
        ),
    ]
