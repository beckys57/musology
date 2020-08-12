# Generated by Django 3.0.5 on 2020-08-09 18:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tech', '0002_auto_20200809_1840'),
        ('locations', '0012_auto_20200809_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='locationfeature',
            name='tech',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tech.Tech'),
        ),
    ]
