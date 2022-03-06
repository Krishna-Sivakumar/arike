from django.http import HttpResponseRedirect
from django.views import generic

from care.forms import TreatmentForm
from care.models import Treatment, Patient, TreatmentNotes

from .mixins import TitleMixin, UserAccessMixin


class PatientAuthorizationMixin:

    def get_queryset(self):
        nurse = self.request.user
        return Treatment.objects.filter(patient__facility=nurse.facility, deleted=False)


class ListTreatments(PatientAuthorizationMixin, generic.ListView):
    template_name = "treatment/list.html"


class CreateTreatment(UserAccessMixin, TitleMixin, PatientAuthorizationMixin, generic.edit.CreateView):
    title = "add treatment"
    template_name = "user/form.html"
    form_class = TreatmentForm

    def get_success_url(self):
        return f"/patient/{self.kwargs.get('pk')}/treatment/"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.patient = Patient.objects.get(pk=self.kwargs.get("pk"))
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class DetailTreatment(UserAccessMixin, PatientAuthorizationMixin, generic.DetailView):
    template_name = "treatment/details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        context.update({
            "notes": TreatmentNotes.objects.filter(deleted=False, treatment=self.object)
        })
        return context


class UpdateTreatment(UserAccessMixin, TitleMixin, PatientAuthorizationMixin, generic.edit.UpdateView):
    title = "update treatment"
    template_name = "user/form.html"
    form_class = TreatmentForm

    def get_success_url(self):
        return f"/patient/{self.kwargs.get('pk')}/treatment/"


class DeleteTreatment(UserAccessMixin, TitleMixin, PatientAuthorizationMixin, generic.edit.DeleteView):
    title = "delete treatment"
    form_class = TreatmentForm
    template_name = "user/form.html"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.deleted = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return f"/patient/{self.kwargs.get('pk')}/treatment/"


class CreateTreatmentNote(UserAccessMixin, TitleMixin, PatientAuthorizationMixin, generic.edit.CreateView):
    title = "add notes"
    template_name = "user/form.html"
    success_url = "/visit/"
    model = TreatmentNotes
    fields = ("note", "visit")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        treatment = Treatment.objects.get(pk=self.kwargs.get("pk"))
        context.update({
            "treatment": treatment
        })
        return context

    def form_valid(self, form):
        treatment = Treatment.objects.get(pk=self.kwargs.get("pk"))

        self.object = form.save(commit=False)
        self.object.user = self.request.user

        self.object.treatment = treatment
        self.object.description = treatment.description
        self.object.care_type = treatment.care_type

        self.object.save()

        return HttpResponseRedirect(self.get_success_url())
