# Generated by Django 3.0.2 on 2020-02-04 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quake',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.CharField(max_length=100)),
                ('Latitude', models.FloatField()),
                ('Longitude', models.FloatField()),
                ('Type', models.CharField(max_length=100)),
                ('Depth', models.FloatField()),
                ('Magnitude', models.FloatField()),
                ('Magnitude_Type', models.CharField(max_length=100)),
                ('ID', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Quake',
            },
        ),
    ]
