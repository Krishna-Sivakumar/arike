from django.contrib.auth.views import LogoutView
from django.urls import path

import care.views

urlpatterns = [
    path("", care.views.Home.as_view(), name="home"),
    path("user/login/", care.views.UserLogin.as_view()),
    path("user/logout/", LogoutView.as_view()),
    path("facility", care.views.ListFacilities.as_view())
] + [
    # Patient Views
    path("patient/", care.views.PatientList.as_view()),
    path("patient/create", care.views.PatientCreate.as_view()),
    path("patient/<pk>/", care.views.PatientDetails.as_view()),
    path("patient/<pk>/edit/", care.views.PatientUpdate.as_view()),
]
