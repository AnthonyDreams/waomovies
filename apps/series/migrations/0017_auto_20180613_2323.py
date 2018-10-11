# Generated by Django 2.0.5 on 2018-06-14 03:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('series', '0016_auto_20180613_2006'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vermastarde',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateField(auto_now=True)),
                ('favoritos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('serie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='series.Series')),
            ],
        ),
        migrations.AlterField(
            model_name='votacion',
            name='series',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='series_id', to='series.Series'),
        ),
    ]
