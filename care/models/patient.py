from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from arike.users.models import User

from .basic import FAMILY_RELATION_CHOICES, GENDER_CHOICES, BaseModel
from .organization import Facility, Ward


class Patient(BaseModel):
    full_name = models.CharField(max_length=100, null=False, blank=False)
    date_of_birth = models.DateField(null=False, blank=False)
    address = models.TextField(null=False, blank=False)
    phone = models.CharField(max_length=10, null=False, blank=False)
    landmark = models.CharField(max_length=150, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=False, blank=False)
    emergency_phone_number = models.CharField(max_length=10, null=False, blank=False)
    expired_time = models.DateTimeField(null=True, blank=True)

    chc_nurse = models.ForeignKey(
        User,
        verbose_name="Refer to Nurse",
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING
    )
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT)
    facility = models.ForeignKey(Facility, on_delete=models.PROTECT)


class FamilyDetails(BaseModel):

    full_name = models.CharField(max_length=100, null=False, blank=False)
    phone = models.CharField(max_length=10, null=False, blank=False)
    date_of_birth = models.DateField(null=False, blank=False)
    email = models.EmailField(null=True, blank=True)
    relation = models.CharField(max_length=20, choices=FAMILY_RELATION_CHOICES)
    address = models.TextField(null=False, blank=False)
    education = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    remarks = models.TextField(max_length=100)
    is_primary = models.BooleanField(default=False)

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)


@receiver(post_save, sender=Patient)
def updateReport(instance, **kwargs):
    send_mail(
        "subject",
        "message",
        "hospital@hospital.com",
        [
            member.email
            for member in
            FamilyDetails.objects.filter(patient=instance, deleted=False)
        ]
    )
