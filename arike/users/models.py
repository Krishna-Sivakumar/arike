from django.contrib.auth.models import AbstractUser
from django.db.models import (
    PROTECT,
    BooleanField,
    CharField,
    DateTimeField,
    EmailField,
    ForeignKey,
)
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for arike.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    roles = (
        ("PN", "Primary Nurse"),
        ("SN", "Secondary Nurse"),
        ("DA", "District Admin"),
    )

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), null=False, blank=False, max_length=255)
    first_name = CharField(max_length=255, blank=True)
    last_name = CharField(max_length=255, blank=True)

    email = EmailField(null=False, blank=False)
    role = CharField(max_length=3, choices=roles, null=False, blank=False)
    phone = CharField(max_length=10, null=False, blank=False)
    is_verified = BooleanField(default=False)
    date_of_birth = DateTimeField(null=True, blank=True)

    district = ForeignKey("care.District", null=True, on_delete=PROTECT)
    facility = ForeignKey("care.Facility", null=True, blank=True, on_delete=PROTECT)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
