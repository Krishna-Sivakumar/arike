from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views import generic

from care.forms import FamilyForm
from care.models import FamilyDetails, Patient


class FamilyEditMixin:
    form_class = FamilyForm

    def get_queryset(self):
        return FamilyDetails.objects.filter(
            patient__pk=self.kwargs.get("pk"),
            deleted=False
        )

    def get_success_url(self):
        pk = self.object.patient.pk
        return f"/patient/{pk}/family"


class ListFamily(LoginRequiredMixin, generic.ListView):

    template_name = "family/list.html"

    def get_queryset(self):
        return FamilyDetails.objects.filter(
            patient__pk=self.kwargs.get("pk"),
            deleted=False
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "patient": Patient.objects.get(pk=self.kwargs.get("pk"))
        })
        return context


class CreateFamily(LoginRequiredMixin, FamilyEditMixin, generic.edit.CreateView):
    template_name = "family/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "head": "create family detail"
        })
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.patient = Patient.objects.get(pk=self.kwargs.get("pk"))
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class UpdateFamily(LoginRequiredMixin, FamilyEditMixin, generic.edit.UpdateView):
    template_name = "family/form.html"

    def get_queryset(self):
        return FamilyDetails.objects.filter(
            deleted=False,
            patient__facility=self.request.user.facility
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "head": "edit family detail"
        })
        return context


class DeleteFamily(LoginRequiredMixin, FamilyEditMixin, generic.edit.DeleteView):

    template_name = "family/form.html"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.deleted = True
        self.object.save()
        return HttpResponseRedirect(
            self.get_success_url()
        )

    def get_queryset(self):
        return FamilyDetails.objects.filter(
            deleted=False,
            patient__facility=self.request.user.facility
        )
