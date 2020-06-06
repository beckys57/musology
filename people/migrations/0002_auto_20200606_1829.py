# Generated by Django 3.0.5 on 2020-06-06 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='hair_color',
            field=models.CharField(default='#000000', max_length=7),
        ),
        migrations.AddField(
            model_name='person',
            name='hair_style',
            field=models.CharField(default='1', max_length=1),
        ),
        migrations.AddField(
            model_name='person',
            name='shirt_color',
            field=models.CharField(default='#280c38', max_length=7),
        ),
        migrations.AddField(
            model_name='person',
            name='shirt_detail',
            field=models.CharField(default='#6a6b98', max_length=7),
        ),
        migrations.AddField(
            model_name='person',
            name='shirt_style',
            field=models.CharField(default='1', max_length=1),
        ),
    ]