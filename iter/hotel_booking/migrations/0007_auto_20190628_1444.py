# Generated by Django 2.2 on 2019-06-28 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel_booking', '0006_auto_20190626_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotels',
            name='lat',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='hotels',
            name='long',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='hotels'),
        ),
    ]
