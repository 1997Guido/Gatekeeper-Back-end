# Generated by Django 4.1.3 on 2022-11-25 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_passwords'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Passwords',
        ),
    ]
