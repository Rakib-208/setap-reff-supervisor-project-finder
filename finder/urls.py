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
    path(
        "dashboard/interests/add/",
        views.interest_create,
        name="interest-create",
    ),
    path(
        "dashboard/interests/<int:interest_id>/edit/",
        views.interest_update,
        name="interest-update",
    ),
    path(
        "dashboard/interests/<int:interest_id>/delete/",
        views.interest_delete,
        name="interest-delete",
    ),
    path(
        "dashboard/projects/add/",
        views.project_create,
        name="project-create",
    ),
    path(
        "dashboard/projects/<int:project_id>/edit/",
        views.project_update,
        name="project-update",
    ),
    path(
        "dashboard/projects/<int:project_id>/delete/",
        views.project_delete,
        name="project-delete",
    ),
]
