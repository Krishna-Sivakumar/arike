from datetime import datetime

from django.http import HttpResponseRedirect
from django.views import generic

from care.forms import ScheduleVisitForm, VisitDetailForm
from care.models import Treatment, VisitSchedule
from care.models.treatment import TreatmentNotes

from .mixins import TitleMixin, UserAccessMixin


class ScheduleVisit(UserAccessMixin, TitleMixin, generic.edit.CreateView):
    title = "schedule visit"
    template_name = "user/form.html"
    form_class = ScheduleVisitForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.nurse = self.request.user
        self.object.save()

        return HttpResponseRedirect("/visit/")

    def get_queryset(self):
        now = datetime.now()
        return VisitSchedule.objects.filter(
            nurse__facility=self.request.user.facility,
            timestamp__gt=now,
            deleted=False
        )


class UnscheduleVisit(UserAccessMixin, TitleMixin, generic.edit.DeleteView):
    title = "unschedule visit"
    template_name = "user/form.html"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.deleted = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return "/visit/"

    def get_queryset(self):
        now = datetime.now()
        return VisitSchedule.objects.filter(
            nurse__facility=self.request.user.facility,
            timestamp__gt=now,
            deleted=False
        )


class ListVisits(UserAccessMixin, generic.ListView):
    template_name = "visit/list.html"

    def get_queryset(self):
        now = datetime.now()
        return VisitSchedule.objects.filter(
            nurse=self.request.user,
            timestamp__gte=now,
            deleted=False
        )


class VisitDetail(UserAccessMixin, TitleMixin, generic.edit.CreateView):
    form_class = VisitDetailForm
    template_name = "user/form.html"
    success_url = "/visit/"

    title = "patient health information"

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


class ListVisitNotes(UserAccessMixin, generic.ListView):
    template_name = "visit/note_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        visit: VisitSchedule = VisitSchedule.objects.get(pk=self.kwargs.get("pk"))
        context.update({
            "patient": visit.patient
        })
        return context

    def get_queryset(self):
        visit: VisitSchedule = VisitSchedule.objects.get(pk=self.kwargs.get("pk"))
        return Treatment.objects.filter(
            patient=visit.patient,
            deleted=False
        )


class CreateVisitNotes(TitleMixin, generic.edit.CreateView):
    title = "add notes"
    template_name = "user/form.html"

    def get_queryset(self):
        return TreatmentNotes.objects.all()

    def get_queryset(self):
        pass
