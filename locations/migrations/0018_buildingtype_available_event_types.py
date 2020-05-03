# Generated by Django 3.0.5 on 2020-05-03 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_eventtype_slots_required'),
        ('locations', '0017_auto_20200503_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildingtype',
            name='available_event_types',
            field=models.ManyToManyField(through='locations.VenueAssessment', to='events.EventType'),
        ),
    ]