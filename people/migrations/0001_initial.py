# Generated by Django 3.0.5 on 2020-06-04 10:17

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('brand', '0001_initial'),
        ('genres', '0001_initial'),
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('bar staff', 'bar staff'), ('techie', 'techie'), ('roadie', 'roadie'), ('musician', 'musician'), ('teacher', 'teacher'), ('promoter', 'promoter'), ('venue owner', 'venue owner')], max_length=27)),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='brand.Brand')),
                ('workplace', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.Location')),
            ],
            options={
                'verbose_name': 'Cool cat',
                'verbose_name_plural': 'People in the industry',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('stamina', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9)])),
                ('charisma', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9)])),
                ('musical_talent', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9)])),
                ('tech_talent', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9)])),
                ('happiness', models.CharField(choices=[('0', "majorly foo'd off"), ('1', 'really???'), ('2', 'this sucks!!'), ('3', 'meh.'), ('4', "i mean, life's been better"), ('5', 'taking it as it comes'), ('6', 'pretty chill'), ('7', 'in the vibe!'), ('8', 'yeahhh! ROCK OONN!'), ('9', 'cloud 9, this is nirvana, man...')], default='6', max_length=1)),
                ('popularity', models.PositiveSmallIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='genres.Genre')),
                ('job', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='people.Job')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='people', to='locations.Location')),
            ],
            options={
                'verbose_name_plural': 'contacts',
            },
        ),
        migrations.CreateModel(
            name='Musician',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('band', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='musicians', to='brand.Band')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='music_career', to='people.Person')),
            ],
        ),
        migrations.CreateModel(
            name='Crowd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proportion', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('district', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='crowds', to='locations.District')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='genres.Genre')),
            ],
        ),
    ]
