# Generated by Django 3.0.5 on 2020-05-02 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0005_auto_20200502_2310'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='prestige',
            field=models.PositiveSmallIntegerField(default=3),
        ),
        migrations.AddField(
            model_name='location',
            name='running_cost',
            field=models.PositiveSmallIntegerField(default=50),
        ),
    ]