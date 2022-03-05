from django.contrib.auth.mixins import (
    AccessMixin,
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.http import HttpResponseRedirect
from django.views import generic

from arike.users.models import User
from care.forms import CustomForm
from care.models import Patient

from .mixins import TitleMixin


class UserAccessMixin(LoginRequiredMixin, UserPassesTestMixin, AccessMixin):
    def handle_no_permission(self):
        return HttpResponseRedirect("/initial")

    def test_func(self):
        return self.request.user.is_verified is True


class PatientModelView:
    def get_queryset(self):
        nurse: User = self.request.user
        return Patient.objects.filter(facility=nurse.facility, facility__kind="PHC", deleted=False)


class PatientList(UserAccessMixin, generic.ListView):

    template_name = "patient/list.html"

    def get_queryset(self):
        nurse: User = self.request.user
        query_params = {
            "full_name__icontains": self.request.GET.get("name") or "",
            "phone__icontains": self.request.GET.get("phone") or "",
        }

        return Patient.objects.filter(facility=nurse.facility, facility__kind="PHC", **query_params, deleted=False)


class PatientDetails(UserAccessMixin, PatientModelView, generic.DetailView):
    template_name = "patient/details.html"


class PatientCreate(UserAccessMixin, PatientModelView, TitleMixin, generic.edit.CreateView):
    template_name = "patient/patient_form.html"
    form_class = CustomForm
    success_url = "/patient/"
    title = "create patient"


class PatientUpdate(UserAccessMixin, PatientModelView, TitleMixin, generic.edit.UpdateView):
    template_name = "patient/patient_form.html"
    form_class = CustomForm
    title = "update patient"

    def get_success_url(self) -> str:
        return f"/patient/{self.get_object().pk}/"


class PatientDelete(UserAccessMixin, PatientModelView, TitleMixin, generic.edit.DeleteView):

    template_name = "patient/patient_form.html"
    form_class = CustomForm
    title = "delete patient"

    success_url = "/patient/"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.deleted = True
        self.object.save()
        return HttpResponseRedirect(success_url)
