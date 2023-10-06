import random
from decimal import Decimal
from uuid import uuid4

from api.models import Event, User
from django.core.management.base import BaseCommand
from faker import Faker


class Command(BaseCommand):
    help = "Create random users and events for testing"

    def handle(self, *args, **kwargs):
        fake = Faker()

        for i in range(100):
            User.objects.create(
                username=fake.user_name(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                date_of_birth=fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=80),
                email=fake.email(),
                gender=random.choice(["Male", "Female", "Undefined"]),
                QrUid=str(uuid4()),
                # Assuming you have some Image instances created before running this script
                # You can assign a profile picture if you like
            )

        users = User.objects.all()

        for i in range(20):
            event_owner = random.choice(users)
            Event.objects.create(
                EventOwner=event_owner,
                EventTitle=fake.text(max_nb_chars=12),
                EventDate=fake.date_this_year(),
                EventTimeStart=fake.time(),
                EventTimeEnd=fake.time(),
                EventLocation=fake.city(),
                EventDescription=fake.text(max_nb_chars=100),
                EventIsPrivate=random.choice([True, False]),
                EventIsCancelled=random.choice([True, False]),
                EventIsFree=random.choice([True, False]),
                EventPrice=Decimal(random.uniform(0, 100)),
                EventMaxGuests=random.randint(1, 100),
                EventCurrentGuests=random.randint(0, 50),
                EventMinimumAge=random.randint(0, 21),
                EventOrganizer=fake.company(),
            )

        for i in range(20):
            event = random.choice(Event.objects.all())
            event.EventInvitedGuests.add(random.choice(users))

        self.stdout.write(self.style.SUCCESS("Successfully created users and events"))
