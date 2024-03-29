from django.http import HttpResponseRedirect
from django.views import generic

from care.models import Facility, Ward

from .mixins import TitleMixin, UserAccessMixin


class FacilityAccessMixin(UserAccessMixin):
    def handle_no_permission(self):
        return HttpResponseRedirect("/")

    def test_func(self):
        return self.request.user.is_verified is True and self.request.user.role == "DA"


class ListFacilities(FacilityAccessMixin, generic.ListView):
    template_name = "facility/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "wards": Ward.objects.all()
        })
        return context

    def get_queryset(self):
        query_params = {}

        if "facility_kind" in self.request.GET.keys():
            kind = self.request.GET.get("facility_kind")
            if kind != "none":
                query_params["kind"] = self.request.GET.get("facility_kind")

        if "facility_ward" in self.request.GET.keys():
            ward = self.request.GET.get("facility_ward")
            if ward != "none":
                query_params["ward__pk"] = self.request.GET.get("facility_ward")

        print(query_params, Facility.objects.filter(
            **query_params
        ))

        return Facility.objects.filter(
            deleted=False,
            ward__lsg_body__district=self.request.user.district,
            **query_params
        )


class ViewFacility(FacilityAccessMixin, generic.DetailView):
    template_name = "facility/detail.html"

    def get_queryset(self):
        return Facility.objects.filter(
            ward__lsg_body__district=self.request.user.district,
            deleted=False
        )


class UpdateFacility(FacilityAccessMixin, TitleMixin, generic.UpdateView):
    template_name = "user/form.html"
    title = "Update Facility"
    model = Facility
    fields = ("name", "kind", "address", "pincode", "phone", "ward",)

    def get_success_url(self):
        return f"/facility/{self.get_object().pk}/"

    def get_queryset(self):
        return Facility.objects.filter(
            ward__lsg_body__district=self.request.user.district,
            deleted=False
        )


class DeleteFacility(FacilityAccessMixin, TitleMixin, generic.DeleteView):
    template_name = "user/form.html"
    model = Facility

    def get_success_url(self):
        return "/facility/"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.deleted = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_title(self):
        return f"Delete {self.get_object()}"

    def get_queryset(self):
        return Facility.objects.filter(
            ward__lsg_body__district=self.request.user.district,
            deleted=False
        )


class CreateFacility(FacilityAccessMixin, TitleMixin, generic.CreateView):
    template_name = "user/form.html"
    model = Facility
    fields = ("kind", "name", "address", "pincode", "phone", "ward")
    success_url = "/facility/"
    title = "create facility"
