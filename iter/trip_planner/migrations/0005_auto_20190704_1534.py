# Generated by Django 2.1 on 2019-07-04 10:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip_planner', '0004_place_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='close_time',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(24)]),
        ),
        migrations.AlterField(
            model_name='place',
            name='open_time',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(24)]),
        ),
        migrations.AlterField(
            model_name='place',
            name='preferred_time',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(24)]),
        ),
        migrations.AlterField(
            model_name='place',
            name='stay_time',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(24)]),
        ),
    ]
