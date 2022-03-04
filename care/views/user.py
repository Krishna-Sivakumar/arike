
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
from care.models import TemporaryLink


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


class CreateUser(UserAccessMixin, generic.edit.CreateView):
    form_class = UserForm
    template_name = "user/form.html"
    success_url = "/user/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "head": "Register Nurse"
        })
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.district = self.request.user.district
        self.object.save()

        temp_link = TemporaryLink(user=self.object)
        temp_link.save()

        send_mail(
            "Onboarding Email",
            f"Click this link to set your password: https://arike.com/temp?token={temp_link.token}",
            from_email="admin@arike.com",
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


class UpdateUser(UserAccessMixin, generic.edit.UpdateView):
    template_name = "user/form.html"
    form_class = UserForm
    success_url = "/user/"

    def get_queryset(self):
        return User.objects.filter(
            Q(district=self.request.user.district) & ~Q(role="DA")
        )


class AssignFacility(UserAccessMixin, generic.edit.UpdateView):
    template_name = "user/form.html"
    fields = ("facility",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "head": "Assign Facility"
        })
        return context

    def get_queryset(self):
        return User.objects.filter(
            Q(district=self.request.user.district) & ~Q(role="DA")
        )


class DeleteUser(UserAccessMixin, generic.edit.DeleteView):

    template_name = "user/form.html"
    success_url = "/user/"

    def get_queryset(self):
        return User.objects.filter(
            Q(district=self.request.user.district) & ~Q(role="DA")
        )
