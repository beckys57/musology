# Generated by Django 3.0.5 on 2020-05-10 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brand', '0016_auto_20200503_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='influence',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='recordlabel',
            name='influence',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]