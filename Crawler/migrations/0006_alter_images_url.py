# Generated by Django 3.2.16 on 2022-11-19 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Crawler', '0005_auto_20221102_0400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='url',
            field=models.CharField(max_length=5000, unique=True),
        ),
    ]
