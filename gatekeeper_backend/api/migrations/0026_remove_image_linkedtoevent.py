# Generated by Django 4.1.3 on 2023-01-16 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_userprofile_profilepicture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='LinkedToEvent',
        ),
    ]