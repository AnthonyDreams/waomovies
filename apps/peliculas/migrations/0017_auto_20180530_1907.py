# Generated by Django 2.0.5 on 2018-05-30 23:07

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('peliculas', '0016_auto_20180529_2140'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('picture', models.ImageField(upload_to='static')),
            ],
        ),
        migrations.AlterField(
            model_name='tag',
            name='label',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('ACC', 'Acción'), ('DRA', 'Drama'), ('SC', 'Ciencia Ficción'), ('TER', 'Terror'), ('SUS', 'Suspenso'), ('CRI', 'Crimen'), ('#MARVEL', 'Marvel')], max_length=30),
        ),
        migrations.RemoveField(
            model_name='trailers',
            name='reparto',
        ),
        migrations.AddField(
            model_name='trailers',
            name='reparto',
            field=models.ManyToManyField(blank=True, null=True, to='peliculas.Cast'),
        ),
    ]
