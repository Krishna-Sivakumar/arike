from django.http import HttpResponseRedirect
from django.views import generic

from care.models import VisitDetails, VisitSchedule
from datetime import datetime

from .mixins import TitleMixin, UserAccessMixin


class ScheduleVisit(UserAccessMixin, TitleMixin, generic.edit.CreateView):
    title = "schedule visit"
    template_name = "user/form.html"
    model = VisitSchedule
    fields = ("timestamp", "duration", "patient")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.nurse = self.request.user

        return HttpResponseRedirect("/visit/")

    def get_queryset(self):
        now = datetime.now()
        return VisitSchedule.objects.filter(nurse__facility=self.request.user.facility, timestamp__gt=now)


class ListVisits(UserAccessMixin, generic.ListView):
    template_name = "visit/list.html"

    def get_queryset(self):
        return VisitSchedule.objects.filter(nurse__facility=self.request.user.facility)


class VisitDetail(generic.edit.CreateView):
    title = "patient health information"
    template_name = "user/form.html"


class ListVisitNotes(generic.ListView):
    pass


class CreateVisitNotes(TitleMixin, generic.edit.CreateView):
    title = "add notes"
    template_name = "user/form.html"
