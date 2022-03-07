import os

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from care.models import FamilyDetails, Patient, Treatment


@receiver(post_save, sender=Patient)
def updateReport(instance, **kwargs):

    treatment_summary = f"""
Summary of {instance.full_name}'s treatment:
{os.linesep.join([f"[{treatment.created_at}] {treatment.care_type}: {treatment.description} " for treatment in Treatment.objects.filter(patient = instance, deleted=False)])}
    """

    send_mail(
        "subject",
        treatment_summary,
        "hospital@hospital.com",
        [
            member.email
            for member in
            FamilyDetails.objects.filter(patient=instance, deleted=False)
        ]
    )
