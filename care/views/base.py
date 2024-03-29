from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.views import generic

from care.forms import CustomForm, ScheduleReportForm
from care.models import TemporaryLink, Report

from datetime import datetime, timedelta

from .mixins import TitleMixin

# Create your views here.


class Home(LoginRequiredMixin, generic.TemplateView):
    template_name = "home.html"


class UserLogin(LoginView):
    pass


class Profile(LoginRequiredMixin, generic.edit.FormView):
    template_name = "profile.html"
    success_url = "/profile"
    form_class = CustomForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "report_id": Report.objects.filter(user=self.request.user)[0].pk,
        })
        return context

    def get_form(self):
        return PasswordChangeForm(self.request.user, self.request.POST)

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        return HttpResponseRedirect(self.get_success_url())


class ScheduleReportView(LoginRequiredMixin, TitleMixin, generic.edit.UpdateView):
    form_class = ScheduleReportForm
    success_url = "/profile"
    template_name = "user/form.html"
    title = "Schedule Report"

    queryset = Report.objects.all()

    def form_valid(self, form):
        self.object = form.save()

        # last_updated is set to the same day so that the next report is sent the following day

        target = datetime.now().replace(hour=self.object.time.hour,
                                        minute=self.object.time.minute, second=0).time()

        self.object.last_updated = datetime.now().replace(
            hour=self.object.time.hour,
            minute=self.object.time.minute,
            second=0
        ) - (
            # last_updated is set to the day before if the current time hasn't passed the report time
            timedelta(days=1) if target >= datetime.now().time()
            else timedelta(days=0)
        )

        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class InitialPassword(LoginRequiredMixin, generic.edit.FormView):
    template_name = "user/form.html"
    success_url = "/profile"
    form_class = CustomForm

    def get_form(self):
        return SetPasswordForm(self.request.user, self.request.POST)

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        user.is_verified = True
        user.save()

        TemporaryLink.objects.get(user=user).delete()

        return HttpResponseRedirect(self.get_success_url())


class TemporaryLogin(generic.View):

    def get(self, request, *args, **kwargs):
        token = request.GET.get("token")
        print(token)
        temporary = TemporaryLink.objects.filter(token=token).first()
        print(temporary)
        if temporary is not None:
            login(request, temporary.user, backend="django.contrib.auth.backends.ModelBackend")
            return HttpResponseRedirect("/initial/")
        else:
            return HttpResponseRedirect("/")
