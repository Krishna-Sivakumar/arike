from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from arike.users.models import User
from care.models import Patient


class PatientModelView:
    model = Patient

    def get_queryset(self):
        nurse: User = self.request.user
        return Patient.objects.filter(facility=nurse.facility)


class PatientList(generic.ListView, LoginRequiredMixin):

    template_name = "patient/list.html"

    def get_queryset(self):
        nurse: User = self.request.user
        query_params = {
            "full_name__icontains": self.request.GET.get("name") or "",
            "phone__icontains": self.request.GET.get("phone") or "",
        }

        return Patient.objects.filter(facility=nurse.facility, **query_params)


class PatientDetails(PatientModelView, generic.DetailView, LoginRequiredMixin):
    template_name = "patient/details.html"


class PatientCreate(PatientModelView, generic.edit.CreateView, LoginRequiredMixin):
    template_name = ""
    fields = "__all__"


class PatientUpdate(PatientModelView, generic.edit.UpdateView, LoginRequiredMixin):
    template_name = ""
    fields = "__all__"
