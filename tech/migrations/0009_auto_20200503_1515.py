# Generated by Django 3.0.5 on 2020-05-03 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tech', '0008_auto_20200503_0111'),
    ]

    operations = [
        migrations.AddField(
            model_name='tech',
            name='category',
            field=models.CharField(blank=True, choices=[('event', 'event'), ('instruments', 'instruments'), ('location', 'location')], max_length=27, null=True),
        ),
        migrations.AddField(
            model_name='tech',
            name='progress',
            field=models.CharField(choices=[('event', 'event'), ('instruments', 'instruments'), ('location', 'location')], default=0, max_length=27),
        ),
    ]