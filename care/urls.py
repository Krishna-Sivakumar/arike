from django.contrib.auth.views import LogoutView
from django.urls import path

import care.views
from care.views.base import Profile

urlpatterns = [
    path("", care.views.Home.as_view(), name="home"),
    path("user/login/", care.views.UserLogin.as_view()),
    path("user/logout/", LogoutView.as_view()),
    path("profile", Profile.as_view()),
    path("facility", care.views.ListFacilities.as_view())
] + [
    # Patient Views
    path("patient/", care.views.PatientList.as_view()),
    path("patient/create", care.views.PatientCreate.as_view()),
    path("patient/<pk>/", care.views.PatientDetails.as_view()),
    path("patient/<pk>/edit/", care.views.PatientUpdate.as_view()),
    path("patient/<pk>/delete/", care.views.PatientDelete.as_view()),
    path("patient/<pk>/family/", care.views.ListFamily.as_view())
] + [
    # Family Detail Views
    path("patient/<pk>/family/create/", care.views.CreateFamily.as_view()),
    path("family/<pk>/edit", care.views.UpdateFamily.as_view()),
    path("family/<pk>/delete/", care.views.DeleteFamily.as_view()),
]
