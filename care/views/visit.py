from django.views import generic

from care.models import VisitDetails, VisitSchedule

from .mixins import TitleMixin, UserAccessMixin


class ScheduleVisit(UserAccessMixin, TitleMixin, generic.edit.CreateView):
    title = "schedule visit"


class VisitDetail(generic.edit.CreateView):
    title = "patient health information"


class ListVisitNotes(generic.ListView):
    pass


class CreateVisitNotes(TitleMixin, generic.edit.CreateView):
    title = "add notes"
