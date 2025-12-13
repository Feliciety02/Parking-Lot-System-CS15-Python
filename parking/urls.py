from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("check-in/", views.check_in, name="check_in"),
    path("check-out/", views.check_out, name="check_out"),
    path("session/<int:session_id>/", views.session_detail, name="session_detail"),
]
