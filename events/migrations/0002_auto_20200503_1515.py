# Generated by Django 3.0.5 on 2020-05-03 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('gig', 'gig'), ('tour', 'tour'), ('party', 'party'), ('training', 'training'), ('recording', 'recording')], default='gig', max_length=27)),
            ],
        ),
        migrations.RemoveField(
            model_name='event',
            name='kind',
        ),
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.EventType'),
        ),
    ]