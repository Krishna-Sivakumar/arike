from django.contrib.auth.views import LogoutView
from django.urls import path

import care.views
from care.views.base import InitialPassword, Profile, TemporaryLogin

urlpatterns = [
    path("", care.views.Home.as_view(), name="home"),
    path("user/login/", care.views.UserLogin.as_view()),
    path("user/logout/", LogoutView.as_view()),
    path("profile/", Profile.as_view()),
    path("initial/", InitialPassword.as_view()),
    path("temp", TemporaryLogin.as_view()),
] + [
    # Patient Views
    path("patient/", care.views.PatientList.as_view()),
    path("patient/create", care.views.PatientCreate.as_view()),
    path("patient/<pk>/", care.views.PatientDetails.as_view()),
    path("patient/<pk>/edit/", care.views.PatientUpdate.as_view()),
    path("patient/<pk>/delete/", care.views.PatientDelete.as_view()),
] + [
    # Family Detail Views
    path("patient/<pk>/family/", care.views.ListFamily.as_view()),
    path("patient/<pk>/family/create/", care.views.CreateFamily.as_view()),
    path("family/<pk>/edit", care.views.UpdateFamily.as_view()),
    path("family/<pk>/delete/", care.views.DeleteFamily.as_view()),
] + [
    # User Views
    path("user/", care.views.ListUsers.as_view()),
    path("user/create/", care.views.CreateUser.as_view()),
    path("user/<pk>/", care.views.UserDetail.as_view()),
    path("user/<pk>/edit/", care.views.UpdateUser.as_view()),
    path("user/<pk>/delete/", care.views.DeleteUser.as_view()),
    path("user/<pk>/assign/", care.views.AssignFacility.as_view()),
    path("user/<pk>/report", care.views.ScheduleReportView.as_view()),
] + [
    # Treatment Views
    path("patient/<pk>/treatment/", care.views.ListTreatments.as_view()),
    path("patient/<pk>/treatment/create", care.views.CreateTreatment.as_view()),
    path("treatment/<pk>/edit/", care.views.UpdateTreatment.as_view()),
    path("treatment/<pk>/delete/", care.views.DeleteTreatment.as_view()),
    path("treatment/<pk>/", care.views.DetailTreatment.as_view()),
    path("treatment/<pk>/add-note", care.views.CreateTreatmentNote.as_view()),
] + [
    # Visitation Views
    path("visit/", care.views.ListVisits.as_view()),
    path("visit/schedule", care.views.ScheduleVisit.as_view()),
    path("visit/<pk>/delete/", care.views.UnscheduleVisit.as_view()),
    path("visit/<pk>/notes/", care.views.ListVisitNotes.as_view()),
    path("visit/<pk>/edit/", care.views.VisitDetail.as_view())
] + [
    # Disease Views
    path("patient/<pk>/disease/", care.views.ListDiseaseHistory.as_view()),
    path("patient/<pk>/disease/create", care.views.CreateDiseaseHistory.as_view()),
    path("disease/<pk>/edit", care.views.UpdateDiseaseHistory.as_view()),
    path("disease/<pk>/delete", care.views.DeleteDiseaseHistory.as_view()),
] + [
    # Facility Views
    path("facility/", care.views.ListFacilities.as_view()),
    path("facility/<pk>/", care.views.ViewFacility.as_view()),
    path("facility/<pk>/edit", care.views.UpdateFacility.as_view()),
    path("facility/<pk>/delete", care.views.DeleteFacility.as_view()),
]
