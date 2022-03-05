from django.contrib.auth.mixins import (
    AccessMixin,
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.http import HttpResponseRedirect
from django.views import generic

from care.forms import FamilyForm
from care.models import FamilyDetails, Patient

from .mixins import TitleMixin


class UserAccessMixin(LoginRequiredMixin, UserPassesTestMixin, AccessMixin):
    def handle_no_permission(self):
        return HttpResponseRedirect("/intial")

    def test_func(self):
        return self.request.user.is_verified is True


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


class CreateFamily(UserAccessMixin, FamilyEditMixin, TitleMixin, generic.edit.CreateView):
    template_name = "family/form.html"
    title = "create family detail"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.patient = Patient.objects.get(pk=self.kwargs.get("pk"))
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class UpdateFamily(UserAccessMixin, FamilyEditMixin, TitleMixin, generic.edit.UpdateView):
    template_name = "family/form.html"

    def get_queryset(self):
        return FamilyDetails.objects.filter(
            deleted=False,
            patient__facility=self.request.user.facility
        )

    def get_title(self):
        return f"edit {self.get_object().full_name}"


class DeleteFamily(UserAccessMixin, FamilyEditMixin, generic.edit.DeleteView):

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
