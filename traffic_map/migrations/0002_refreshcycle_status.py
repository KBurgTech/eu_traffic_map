# Generated by Django 3.2.8 on 2021-10-11 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('traffic_map', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='refreshcycle',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
