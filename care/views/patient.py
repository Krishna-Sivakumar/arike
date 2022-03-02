from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views import generic

from arike.users.models import User
from care.forms import CustomForm
from care.models import Patient


class PatientModelView:
    def get_queryset(self):
        nurse: User = self.request.user
        return Patient.objects.filter(facility=nurse.facility, deleted=False)


class PatientList(LoginRequiredMixin, generic.ListView):

    template_name = "patient/list.html"

    def get_queryset(self):
        nurse: User = self.request.user
        query_params = {
            "full_name__icontains": self.request.GET.get("name") or "",
            "phone__icontains": self.request.GET.get("phone") or "",
        }

        return Patient.objects.filter(facility=nurse.facility, **query_params, deleted=False)


class PatientDetails(LoginRequiredMixin, PatientModelView, generic.DetailView):
    template_name = "patient/details.html"


class PatientCreate(LoginRequiredMixin, PatientModelView, generic.edit.CreateView):
    template_name = "patient/patient_form.html"
    form_class = CustomForm
    success_url = "/patient/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "head": "create patient"
        })
        return context


class PatientUpdate(LoginRequiredMixin, PatientModelView, generic.edit.UpdateView):
    template_name = "patient/patient_form.html"
    form_class = CustomForm

    def get_success_url(self) -> str:
        return f"/patient/{self.get_object().pk}/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "head": "update patient"
        })
        return context


class PatientDelete(LoginRequiredMixin, PatientModelView, generic.edit.DeleteView):

    template_name = "patient/patient_form.html"
    form_class = CustomForm

    success_url = "/patient/"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.deleted = True
        self.object.save()
        return HttpResponseRedirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "head": "delete patient"
        })
        return context
