# Generated by Django 4.1.2 on 2022-10-31 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Crawler', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='webpages',
            name='keywords',
            field=models.CharField(default=0, max_length=1000),
            preserve_default=False,
        ),
    ]
