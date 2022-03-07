from django import forms

from arike.users.models import User
from care.models import (
    FamilyDetails,
    Patient,
    PatientDisease,
    Treatment,
    VisitDetails,
    VisitSchedule,
    Report
)


class BaseFormMixin():

    address = forms.CharField(widget=forms.Textarea({"rows": 3}))

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        kwargs["label_suffix"] = ""
        super().__init__(*args, **kwargs)


class CustomForm(BaseFormMixin, forms.ModelForm):

    address = forms.CharField(widget=forms.Textarea({"rows": 3}))

    class Meta:
        model = Patient
        fields = "__all__"
        exclude = ("deleted", )


class FamilyForm(BaseFormMixin, forms.ModelForm):

    class Meta:
        model = FamilyDetails
        fields = "__all__"
        exclude = ("deleted", "patient")

    address = forms.CharField(widget=forms.Textarea({"rows": 3}))
    remarks = forms.CharField(widget=forms.Textarea({"rows": 3}))


class UserForm(BaseFormMixin, forms.ModelForm):

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "date_of_birth", "facility", "role")

    role = forms.ChoiceField(choices=User.roles[:2])


class TreatmentForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = Treatment
        fields = ("description", "care_type")
        exclude = ("deleted", "patient")

    description = forms.CharField(widget=forms.Textarea({"rows": 3}))


class PatientDiseaseForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = PatientDisease
        fields = ("disease", "treatment", "note")


class ScheduleVisitForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = VisitSchedule
        fields = ("timestamp", "duration", "patient")

    timestamp = forms.DateTimeField(widget=forms.DateTimeInput({"type": "datetime-local"}))


class VisitDetailForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = VisitDetails
        fields = "__all__"
        exclude = ("deleted", )

    pain = forms.BooleanField(widget=forms.NullBooleanSelect(), label="Is the patient in pain?")
    patient_at_peace = forms.BooleanField(widget=forms.NullBooleanSelect(), label="Is the patient at peace?")


class ScheduleReportForm(BaseFormMixin, forms.ModelForm):

    time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={"type": "time"}
        ),
        required=True,
        help_text="<small><em>Use UTC time</em></small>"
    )

    disabled = forms.BooleanField(
        widget=forms.CheckboxInput(),
        label="Disable daily reports",
        required=False
    )

    class Meta:
        model = Report
        fields = ["time", "disabled"]
