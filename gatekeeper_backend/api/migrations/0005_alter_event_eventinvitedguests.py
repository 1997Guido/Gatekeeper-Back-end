# Generated by Django 4.1.3 on 2023-09-29 12:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0004_alter_user_qruid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="EventInvitedGuests",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="invited_to_events",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]