# Generated by Django 2.0.5 on 2018-11-30 02:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notificaciones', '0009_auto_20181128_0848'),
    ]

    operations = [
        migrations.AddField(
            model_name='compartir',
            name='user_who_read',
            field=models.ManyToManyField(related_name='user_who_read', to=settings.AUTH_USER_MODEL),
        ),
    ]