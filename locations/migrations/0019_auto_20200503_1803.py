# Generated by Django 3.0.5 on 2020-05-03 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0018_buildingtype_available_event_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venueassessment',
            name='suitability',
            field=models.PositiveSmallIntegerField(),
        ),
    ]