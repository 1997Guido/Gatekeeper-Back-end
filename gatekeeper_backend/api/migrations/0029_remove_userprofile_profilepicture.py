# Generated by Django 4.1.3 on 2023-01-19 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_event_eventiscancelled'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='profilepicture',
        ),
    ]