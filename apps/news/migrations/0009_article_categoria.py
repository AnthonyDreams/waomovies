# Generated by Django 2.0.5 on 2018-12-30 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_auto_20181229_2248'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='categoria',
            field=models.CharField(choices=[('Noticias', 'Noticias'), ('Critica', 'Crítica'), ('Global', 'Global')], max_length=20, null=True),
        ),
    ]
