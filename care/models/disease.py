from django.db import models

from arike.users.models import User

from .basic import BaseModel
from .patient import Patient
from .treatment import Treatment


class Disease(BaseModel):

    patients = models.ManyToManyField(Patient, through='PatientDisease')

    name = models.CharField(max_length=100, null=False, blank=False)
    icds_code = models.CharField(max_length=6, null=False, blank=False)


class PatientDisease(BaseModel):
    note = models.TextField(blank=True, null=True)
    nurse = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    treatment = models.ForeignKey(Treatment, on_delete=models.DO_NOTHING, blank=True, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.PROTECT)
