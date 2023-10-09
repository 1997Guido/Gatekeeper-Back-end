# factories.py
import factory
from api.models import Event, User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    QrUid = factory.Faker("uuid4")
    password = factory.PostGenerationMethodCall("set_password", "default_password")
    # Add other fields if necessary


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    # Add fields if necessary for the Event model
