# Generated by Django 4.1.3 on 2023-09-28 16:27

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(blank=True, null=True, verbose_name="last login"),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={"unique": "A user with that username already exists."},
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                        verbose_name="username",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(default=django.utils.timezone.now, verbose_name="date joined"),
                ),
                (
                    "name",
                    models.CharField(blank=True, max_length=255, verbose_name="Name of User"),
                ),
                ("first_name", models.CharField(default="John", max_length=30)),
                ("last_name", models.CharField(default="Doe", max_length=30)),
                ("date_of_birth", models.DateField(default="2000-01-01")),
                ("email", models.EmailField(max_length=254)),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("Male", "Male"),
                            ("Female", "Female"),
                            ("Undefined", "Undefined"),
                        ],
                        default=False,
                        max_length=15,
                    ),
                ),
                ("QrUid", models.CharField(default=0, max_length=8)),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Image", models.ImageField(upload_to="images")),
                ("Title", models.CharField(default="Image", max_length=50)),
                ("Description", models.CharField(max_length=100, null=True)),
                (
                    "Owner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="owned_images",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("EventTitle", models.CharField(max_length=12)),
                ("EventDate", models.DateField()),
                ("EventTimeStart", models.TimeField()),
                ("EventTimeEnd", models.TimeField()),
                ("EventLocation", models.CharField(max_length=50)),
                ("EventDescription", models.CharField(max_length=100)),
                ("EventIsPrivate", models.BooleanField(default=False)),
                ("EventIsCancelled", models.BooleanField(default=False)),
                ("EventIsFree", models.BooleanField(default=False)),
                (
                    "EventPrice",
                    models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5),
                ),
                ("EventMaxGuests", models.IntegerField(default=50)),
                ("EventCurrentGuests", models.IntegerField(default=0)),
                ("EventMinimumAge", models.IntegerField(default=0)),
                ("EventOrganizer", models.CharField(max_length=50)),
                (
                    "EventBanner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="event_banners",
                        to="api.image",
                    ),
                ),
                (
                    "EventInvitedGuests",
                    models.ManyToManyField(related_name="invited_to_events", to=settings.AUTH_USER_MODEL),
                ),
                (
                    "EventOwner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="owned_events",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="ProfilePicture",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="profile_picture",
                to="api.image",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                related_name="user_set",
                related_query_name="user",
                to="auth.group",
                verbose_name="groups",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.permission",
                verbose_name="user permissions",
            ),
        ),
    ]
