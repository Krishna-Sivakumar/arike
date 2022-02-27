from django.urls import path
import care.views

urlpatterns = [
    path("", care.views.HomeView.as_view(), name="home"),
]
