from django.http import HttpResponseRedirect
from django.views import generic

from care.models import PatientDisease, Patient

from .mixins import TitleMixin, UserAccessMixin

from care.forms import PatientDiseaseForm


class ListDiseaseHistory(UserAccessMixin, generic.ListView):
    template_name = "disease/list.html"

    def get_queryset(self):
        return PatientDisease.objects.filter(
            deleted=False,
            patient=self.kwargs.get("pk"),
            patient__facility=self.request.user.facility
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "patient": Patient.objects.get(pk=self.kwargs.get("pk"))
        })
        return context


class CreateDiseaseHistory(UserAccessMixin, TitleMixin, generic.edit.CreateView):
    title = "add disease history"
    template_name = "user/form.html"
    form_class = PatientDiseaseForm

    def get_success_url(self):
        return f"/patient/{self.kwargs.get('pk')}/disease/"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.patient = Patient.objects.get(pk=self.kwargs.get("pk"))
        self.object.nurse = self.request.user
        return HttpResponseRedirect(self.get_success_url)

    def get_queryset(self):
        return PatientDisease.objects.filter(
            deleted=False,
            patient__facility=self.request.user.facility
        )


class DeleteDiseaseHistory(UserAccessMixin, TitleMixin, generic.DeleteView):
    title = "delete patient history"
    template_name = "user/form.html"

    def get_queryset(self):
        return PatientDisease.objects.filter(
            deleted=False,
            patient__facility=self.request.user.facility
        )

    def get_success_url(self):
        return f"/patient/{self.kwargs.get('pk')}/disease/"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.deleted = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class UpdateDiseaseHistory(UserAccessMixin, TitleMixin, generic.edit.UpdateView):
    title = "edit disease history"
    template_name = "user/form.html"
    form_class = PatientDiseaseForm

    def get_success_url(self):
        return f"/patient/{self.kwargs.get('pk')}/disease/"

    def get_queryset(self):
        return PatientDisease.objects.filter(
            deleted=False,
            patient__facility=self.request.user.facility
        )
