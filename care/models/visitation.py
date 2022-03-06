from django.db import models

from arike.users.models import User

from .basic import (
    PALLIATIVE_PHASE,
    SYMPTOM_CHOICES,
    SYSTEMIC_EXAMINATION_CHOICES,
    BaseModel,
)
from .patient import Patient


class VisitSchedule(BaseModel):
    timestamp = models.DateTimeField(null=False, blank=False)
    duration = models.TimeField(null=False, blank=False)

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    nurse = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class VisitDetails(BaseModel):

    palliative_phase = models.CharField(max_length=100, choices=PALLIATIVE_PHASE, null=False, blank=False)
    blood_pressure = models.CharField(max_length=7, null=False, blank=False)
    pulse = models.CharField(max_length=7, null=False, blank=False)
    general_random_blood_sugar = models.CharField(max_length=7, null=False, blank=False)
    personal_hygiene = models.TextField(null=False, blank=False)
    mouth_hygiene = models.TextField(null=False, blank=False)
    pubic_hygiene = models.TextField(null=False, blank=False)
    systemic_examination = models.CharField(
        max_length=100, choices=SYSTEMIC_EXAMINATION_CHOICES, null=False, blank=False)
    patient_at_peace = models.BooleanField(default=False)
    pain = models.BooleanField(default=False)
    symptoms = models.CharField(max_length=100, null=True, blank=True, choices=SYMPTOM_CHOICES)
    note = models.TextField()

    schedule = models.ForeignKey(VisitSchedule, on_delete=models.CASCADE)
