# Generated by Django 3.0.5 on 2020-05-03 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0012_auto_20200503_1402'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='district',
            options={'ordering': ['id']},
        ),
        migrations.AlterField(
            model_name='location',
            name='building',
            field=models.CharField(choices=[('music venue', 'music venue'), ('bar', 'bar'), ('club', 'club'), ('record store', 'record store'), ('musical instrument shop', 'musical instrument shop'), ('music lessons', 'music lessons'), ('recording studio', 'recording studio'), ('promo office', 'promo office'), ('workshop', 'workshop'), ('band house', 'band house'), ('park', 'park'), ('empty plot', 'empty plot')], max_length=27),
        ),
    ]
