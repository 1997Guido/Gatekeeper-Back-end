# Generated by Django 4.1.3 on 2023-12-18 11:02

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0009_alter_event_eventbanner"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="EventLocationName",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="EventLocation",
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
    ]
