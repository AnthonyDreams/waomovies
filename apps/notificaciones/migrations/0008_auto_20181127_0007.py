# Generated by Django 2.0.5 on 2018-11-27 04:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notificaciones', '0007_compartir_timestampc'),
    ]

    operations = [
        migrations.RenameField(
            model_name='compartir',
            old_name='user_to_share',
            new_name='users_to_share',
        ),
    ]
