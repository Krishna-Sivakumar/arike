from django.db import models
from .basic import BaseModel, LOCAL_BODY_CHOICES, FACILITY_KIND_CHOICES


class State(BaseModel):
    name = models.CharField(max_length=100, null=False, blank=False)


class District(BaseModel):
    name = models.CharField(max_length=100, null=False, blank=False)
    state = models.ForeignKey(State, on_delete=models.PROTECT, null=False)


class LSGBody(BaseModel):
    name = models.CharField(max_length=100, null=False, blank=False)
    lsg_body_code = models.IntegerField(choices=LOCAL_BODY_CHOICES, null=False)

    district = models.ForeignKey(District, on_delete=models.PROTECT, null=False)


class Ward (BaseModel):
    name = models.CharField(max_length=100, null=False, blank=False)
    number = models.IntegerField()

    lsg_body = models.ForeignKey(LSGBody, on_delete=models.PROTECT, null=False)


class Facility(BaseModel):
    name = models.CharField(max_length=100, null=False, blank=False)
    kind = models.CharField(max_length=3, choices=FACILITY_KIND_CHOICES, null=False, blank=False)
    address = models.TextField(null=False, blank=False)
    pincode = models.CharField(max_length=15, null=False, blank=False)
    phone = models.CharField(max_length=10, null=False, blank=False)

    ward = models.ForeignKey(Ward, on_delete=models.PROTECT)
