# Generated by Django 3.0.5 on 2020-05-02 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locations', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('brand', '0002_auto_20200502_1654'),
        ('genres', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crowd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proportion', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='genres.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='VenueOwner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='brand.Brand')),
                ('workplace', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.Location')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Techie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='brand.Brand')),
                ('workplace', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.Location')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Roadie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='brand.Brand')),
                ('workplace', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.Location')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Promoter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='brand.Brand')),
                ('workplace', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.Location')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Population',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crowds', models.ManyToManyField(through='people.Crowd', to='genres.Genre')),
                ('district', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.District')),
            ],
            options={
                'verbose_name_plural': 'populus',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('birthday', models.DateField()),
                ('job_id', models.PositiveIntegerField(blank=True, null=True)),
                ('happiness', models.CharField(blank=True, max_length=1, null=True)),
                ('influence', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='genres.Genre')),
                ('job_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.Location')),
            ],
            options={
                'verbose_name_plural': 'people',
            },
        ),
        migrations.CreateModel(
            name='Musician',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('band', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='musicians', to='brand.Band')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='brand.Brand')),
                ('workplace', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.Location')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='crowd',
            name='population',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.Population'),
        ),
        migrations.CreateModel(
            name='BarStaff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='brand.Brand')),
                ('workplace', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='locations.Location')),
            ],
            options={
                'verbose_name_plural': 'bar staff',
            },
        ),
    ]
