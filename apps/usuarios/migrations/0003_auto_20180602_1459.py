# Generated by Django 2.0.5 on 2018-06-02 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='perfil_img',
            field=models.ImageField(upload_to='static'),
        ),
    ]
