# Generated by Django 3.0.5 on 2020-05-02 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0003_auto_20200502_1810'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BarStaff',
        ),
        migrations.RemoveField(
            model_name='musician',
            name='band',
        ),
        migrations.DeleteModel(
            name='Promoter',
        ),
        migrations.DeleteModel(
            name='Roadie',
        ),
        migrations.DeleteModel(
            name='Techie',
        ),
        migrations.DeleteModel(
            name='VenueOwner',
        ),
        migrations.DeleteModel(
            name='Musician',
        ),
    ]
