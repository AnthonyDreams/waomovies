# Generated by Django 2.0.5 on 2018-06-14 21:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('peliculas', '0040_auto_20180614_1739'),
        ('series', '0029_auto_20180614_1739'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vermastarde',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('peliculas', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='peliculas.Peliculas')),
                ('series', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='series.Series')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
