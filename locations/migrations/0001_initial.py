# Generated by Django 3.0.5 on 2020-06-04 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('genres', '0001_initial'),
        ('brand', '0001_initial'),
        ('events', '0001_initial'),
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildingType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('concert hall', 'concert hall'), ('music bar', 'music bar'), ('local pub', 'local pub'), ('club', 'club'), ('record store', 'record store'), ('musical instrument shop', 'musical instrument shop'), ('music lessons', 'music lessons'), ('recording studio', 'recording studio'), ('promo office', 'promo office'), ('workshop', 'workshop'), ('band house', 'band house'), ('park', 'park'), ('empty plot', 'empty plot')], max_length=31)),
                ('category', models.CharField(choices=[('venue with stage', 'venue with stage'), ('pub or cafe', 'pub or cafe'), ('shop', 'shop'), ('public place', 'public place'), ('private place', 'private place'), ('training or work', 'training or work')], max_length=31)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127)),
                ('latitude', models.CharField(blank=True, max_length=12, null=True)),
                ('longitude', models.CharField(blank=True, max_length=12, null=True)),
                ('game', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cities', to='game.Game')),
            ],
            options={
                'verbose_name_plural': 'cities',
            },
        ),
        migrations.CreateModel(
            name='VenueAssessment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suitability', models.PositiveSmallIntegerField()),
                ('building_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.BuildingType')),
                ('event_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.EventType')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127)),
                ('latitude', models.CharField(blank=True, max_length=12, null=True)),
                ('longitude', models.CharField(blank=True, max_length=12, null=True)),
                ('slots_available', models.PositiveSmallIntegerField(default=4)),
                ('capacity', models.PositiveSmallIntegerField(blank=True, default=100, null=True)),
                ('popularity', models.PositiveSmallIntegerField(default=0)),
                ('prestige', models.PositiveSmallIntegerField(default=3)),
                ('running_cost', models.PositiveSmallIntegerField(default=50)),
                ('entry_price', models.PositiveSmallIntegerField(default=0)),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='brand.Brand')),
                ('building_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='locations.BuildingType')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='genres.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127)),
                ('population', models.PositiveSmallIntegerField(default=100)),
                ('latitude', models.CharField(blank=True, max_length=12, null=True)),
                ('longitude', models.CharField(blank=True, max_length=12, null=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='districts', to='locations.City')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='buildingtype',
            name='available_event_types',
            field=models.ManyToManyField(through='locations.VenueAssessment', to='events.EventType'),
        ),
    ]
