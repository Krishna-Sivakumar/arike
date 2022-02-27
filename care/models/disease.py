from django.db import models
from .basic import BaseModel
from .patient import Patient


class Disease(BaseModel):

    patients = models.ManyToManyField(Patient, through='PatientDisease')

    name = models.CharField(max_length=100, null=False, blank=False)
    icds_code = models.CharField(max_length=6, null=False, blank=False)


class PatientDisease(BaseModel):
    note = models.TextField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.PROTECT)
