# Generated by Django 2.2 on 2019-06-25 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_booking', '0003_auto_20190617_1204'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotels',
            name='description',
            field=models.CharField(default='Hello', max_length=500),
        ),
    ]