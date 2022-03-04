from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.views import generic

from care.forms import CustomForm
from care.models import Facility, TemporaryLink

# Create your views here.


class Home(LoginRequiredMixin, generic.TemplateView):
    template_name = "home.html"


class ListFacilities(LoginRequiredMixin, generic.ListView):
    template_name = "facility/list.html"
    queryset = Facility.objects.all()


class UserLogin(LoginView):
    pass


class Profile(LoginRequiredMixin, generic.edit.FormView):
    template_name = "profile.html"
    success_url = "/profile"
    form_class = CustomForm

    def get_form(self):
        return PasswordChangeForm(self.request.user, self.request.POST)

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
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
