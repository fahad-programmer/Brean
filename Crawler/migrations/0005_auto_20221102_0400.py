# Generated by Django 3.2.16 on 2022-11-01 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Crawler', '0004_alter_webpages_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webpages',
            name='keywords',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='webpages',
            name='title',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
