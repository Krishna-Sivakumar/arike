from django.db import models
from .basic import BaseModel, TREATMENT_GROUPS
from .patient import Patient
from .visitation import VisitSchedule


class Treatment(BaseModel):

    description = models.TextField(null=False, blank=False)
    care_type = models.CharField(max_length=100, choices=TREATMENT_GROUPS, blank=False, null=False)

    visit = models.ManyToManyField(VisitSchedule, through="TreatmentNotes")
    patient = models.ForeignKey(Patient, on_delete=models.DO_NOTHING)


class TreatmentNotes(BaseModel):

    note = models.TextField()
    description = models.TextField(null=False, blank=False)
    care_type = models.CharField(max_length=100, choices=TREATMENT_GROUPS, blank=False, null=False)

    visit = models.ForeignKey(VisitSchedule, on_delete=models.CASCADE)
    treatment = models.ForeignKey(Treatment, on_delete=models.PROTECT)
