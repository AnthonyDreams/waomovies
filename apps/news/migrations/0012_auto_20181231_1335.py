# Generated by Django 2.0.5 on 2018-12-31 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0011_votacion_articulos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hitcount_Articulos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hitcount_day', models.IntegerField(default=0)),
                ('hitcount_week', models.IntegerField(default=0)),
                ('hitcount_month', models.IntegerField(default=0)),
                ('hitcount_ever', models.IntegerField(default=0)),
                ('publish', models.DateField(auto_now_add=True)),
                ('expired', models.DateTimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='article',
            name='hitcount_day',
        ),
        migrations.RemoveField(
            model_name='article',
            name='hitcount_ever',
        ),
        migrations.RemoveField(
            model_name='article',
            name='hitcount_month',
        ),
        migrations.RemoveField(
            model_name='article',
            name='hitcount_week',
        ),
        migrations.AddField(
            model_name='hitcount_articulos',
            name='articulo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.Article'),
        ),
    ]
