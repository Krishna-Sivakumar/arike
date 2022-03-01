from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views import generic

from care.models import Facility

# Create your views here.


class Home(generic.TemplateView, LoginRequiredMixin):
    template_name = "home.html"


class ListFacilities(generic.ListView, LoginRequiredMixin):
    template_name = "facility/list.html"
    queryset = Facility.objects.all()


class UserLogin(LoginView):
    pass
