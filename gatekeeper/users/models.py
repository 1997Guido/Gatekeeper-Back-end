from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for gatekeeper-backend.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = models.CharField(max_length=30, blank=False, null=False, default="John")
    last_name = models.CharField(max_length=30, blank=False, null=False, default="Doe")
    date_of_birth = models.DateField(null=False, blank=False, default="2000-01-01")
    email = models.EmailField(max_length=254, blank=False, null=False)
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Undefined", "Undefined"),
    )
    gender = models.CharField(max_length=15, choices=GENDER_CHOICES, default=False, null=False)
    QrUid = models.CharField(max_length=8, null=False, default=0)
    ProfilePicture = models.ForeignKey(
        "api.Image", on_delete=models.SET_NULL, blank=True, null=True, related_name="profile_pictures"
    )

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
