# Generated by Django 3.2.5 on 2021-10-10 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LiveItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refresh_cycle', models.IntegerField()),
                ('loc_latitude', models.FloatField()),
                ('loc_longitude', models.FloatField()),
                ('title', models.CharField(max_length=128)),
                ('type', models.CharField(max_length=16)),
                ('data', models.CharField(max_length=2048)),
            ],
        ),
        migrations.CreateModel(
            name='RefreshCycle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finished', models.BooleanField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RoadAccident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refresh_cycle', models.IntegerField()),
                ('loc_latitude', models.FloatField()),
                ('loc_longitude', models.FloatField()),
                ('title', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=2048)),
                ('created_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Roadwork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refresh_cycle', models.IntegerField()),
                ('loc_latitude', models.FloatField()),
                ('loc_longitude', models.FloatField()),
                ('title', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=2048)),
                ('type', models.CharField(max_length=16)),
                ('created_at', models.DateTimeField()),
            ],
        ),
    ]
