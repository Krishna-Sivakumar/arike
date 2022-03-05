from django.db import models

from arike.users.models import User

from .basic import TREATMENT_GROUPS, BaseModel
from .patient import Patient
from .visitation import VisitSchedule


class Treatment(BaseModel):

    description = models.TextField(null=False, blank=False)
    care_type = models.CharField(max_length=100, choices=TREATMENT_GROUPS, blank=False, null=False)

    patient = models.ForeignKey(Patient, on_delete=models.DO_NOTHING)
    nurse = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class TreatmentNotes(BaseModel):

    note = models.TextField()
    description = models.TextField(null=False, blank=False)
    care_type = models.CharField(max_length=100, choices=TREATMENT_GROUPS, blank=False, null=False)

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    visit = models.ForeignKey(VisitSchedule, on_delete=models.CASCADE)
    treatment = models.ForeignKey(Treatment, on_delete=models.PROTECT)
