# Generated by Django 3.0.5 on 2020-06-04 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_location_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='locations', to='locations.District'),
        ),
    ]