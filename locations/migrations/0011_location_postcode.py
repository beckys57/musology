# Generated by Django 3.0.5 on 2020-05-03 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0010_auto_20200503_1237'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='postcode',
            field=models.CharField(choices=[('A1', 'A1'), ('A2', 'A2'), ('A3', 'A3'), ('A4', 'A4'), ('B1', 'B1'), ('B2', 'B2'), ('B3', 'B3'), ('B4', 'B4'), ('C1', 'C1'), ('C2', 'C2'), ('C3', 'C3'), ('C4', 'C4'), ('D1', 'D1'), ('D2', 'D2'), ('D3', 'D3'), ('D4', 'D4')], default='D4', max_length=2),
        ),
    ]
