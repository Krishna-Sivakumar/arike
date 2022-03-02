from django import forms

from care.models import FamilyDetails, Patient


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