# Generated by Django 3.0.5 on 2020-05-02 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0007_auto_20200502_2110'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='title',
            new_name='role',
        ),
    ]
