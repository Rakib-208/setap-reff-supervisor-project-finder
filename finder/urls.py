from django.urls import path

from . import views


app_name = "finder"

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("staff/", views.staff_directory, name="staff-directory"),
    path("staff/<int:profile_id>/", views.staff_profile, name="staff-profile"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
