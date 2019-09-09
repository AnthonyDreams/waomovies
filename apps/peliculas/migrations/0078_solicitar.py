# Generated by Django 2.0.5 on 2019-04-01 01:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('peliculas', '0077_auto_20190329_1832'),
    ]

    operations = [
        migrations.CreateModel(
            name='solicitar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solicitado', models.CharField(max_length=150, unique=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('solicitante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]