# Generated by Django 3.0.5 on 2020-06-14 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0006_auto_20200607_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='popularity',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
