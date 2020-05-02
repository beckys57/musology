# Generated by Django 3.0.5 on 2020-05-02 21:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0010_auto_20200502_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musician',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='band', to='people.Person'),
        ),
    ]
