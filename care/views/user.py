
from django.contrib.auth.mixins import (
    AccessMixin,
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.views import generic

from arike.users.models import User
from care.forms import UserForm
from care.models import TemporaryLink, Report
from config.settings.local import FROM_ADDRESS

from .mixins import TitleMixin


class UserAccessMixin(LoginRequiredMixin, UserPassesTestMixin, AccessMixin):
    def handle_no_permission(self):
        return HttpResponseRedirect("/")

    def test_func(self):
        return self.request.user.role == "DA"


class ListUsers(UserAccessMixin, generic.ListView):
    template_name = "user/list.html"

    def get_queryset(self):
        query_params = {
            "name__icontains": self.request.GET.get("name") or ""
        }
        return User.objects.filter(
            Q(district=self.request.user.district) & ~Q(role="DA") & Q(**query_params)
        )


class CreateUser(UserAccessMixin, TitleMixin, generic.edit.CreateView):
    form_class = UserForm
    template_name = "user/form.html"
    success_url = "/user/"
    title = "Register Nurse"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.district = self.request.user.district
        self.object.save()

        temp_link = TemporaryLink(user=self.object)
        temp_link.save()

        Report.objects.create(user=self.object)

        send_mail(
            "Onboarding Email",
            f"Click this link to set your password: https://arike.com/temp?token={temp_link.token}",
            from_email=FROM_ADDRESS,
            recipient_list=[self.object.email]
        )

        return HttpResponseRedirect(
            self.get_success_url()
        )


class UserDetail(UserAccessMixin, generic.DetailView):

    template_name = "user/details.html"

    def get_queryset(self):
        return User.objects.filter(
            Q(district=self.request.user.district) & ~Q(role="DA")
        )


class UpdateUser(UserAccessMixin, TitleMixin, generic.edit.UpdateView):
    template_name = "user/form.html"
    form_class = UserForm
    success_url = "/user/"

    def get_queryset(self):
        return User.objects.filter(
            Q(district=self.request.user.district) & ~Q(role="DA")
        )

    def get_title(self):
        return f"Update {self.get_object().first_name} {self.get_object().last_name}"


class AssignFacility(UserAccessMixin, TitleMixin, generic.edit.UpdateView):
    template_name = "user/form.html"
    fields = ("facility",)
    title = "Assign Facility"
    success_url = "/user/"

    def get_queryset(self):
        return User.objects.filter(
            Q(district=self.request.user.district) & ~Q(role="DA")
        )


class DeleteUser(UserAccessMixin, TitleMixin, generic.edit.DeleteView):

    template_name = "user/form.html"
    success_url = "/user/"

    def get_title(self):
        return f"Delete {self.get_object().first_name} {self.get_object().last_name}"

    def get_queryset(self):
        return User.objects.filter(
            Q(district=self.request.user.district) & ~Q(role="DA")
        )
