# Generated by Django 2.0.5 on 2018-07-05 14:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0047_auto_20180705_0917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capitulos',
            name='unvote_capitulo',
            field=models.ManyToManyField(blank=True, null=True, related_name='unvote_capitulo', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='capitulos',
            name='vote_capitulo',
            field=models.ManyToManyField(blank=True, null=True, related_name='vote_capitulo', to=settings.AUTH_USER_MODEL),
        ),
    ]
