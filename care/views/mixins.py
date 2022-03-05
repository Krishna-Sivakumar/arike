from django.contrib.auth.mixins import (
    AccessMixin,
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.http import HttpResponseRedirect


class TitleMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "head": self.get_title
        })
        return context

    def get_title(self):
        return self.title


class UserAccessMixin(LoginRequiredMixin, UserPassesTestMixin, AccessMixin):
    def handle_no_permission(self):
        return HttpResponseRedirect("/initial")

    def test_func(self):
        return self.request.user.is_verified is True
