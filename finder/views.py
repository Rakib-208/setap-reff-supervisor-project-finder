from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth import login, logout
from django.db import transaction
from django.db.models import Count, Q, Value
from django.db.models.functions import Concat
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .access import STAFF_ROLE, STUDENT_ROLE, has_role, role_for, role_required
from .demo_accounts import STAFF_ACCOUNTS, STUDENT_ACCOUNTS
from .forms import EmailAuthenticationForm, InterestForm, ProjectIdeaForm
from .models import Interest, ProjectIdea, StaffProfile


def _role_destination(user):
    role = role_for(user)
    if role == STUDENT_ROLE:
        return "finder:staff-directory"
    if role == STAFF_ROLE:
        return "finder:dashboard"
    return None


def home(request):
    if not request.user.is_authenticated:
        return redirect("finder:login")
    destination = _role_destination(request.user)
    if destination:
        return redirect(destination)
    return render(request, "finder/role_missing.html", status=403)


def login_view(request):
    if request.user.is_authenticated:
        destination = _role_destination(request.user)
        if destination:
            return redirect(destination)

    form = EmailAuthenticationForm(request=request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        destination = _role_destination(user)
        if destination is None:
            form.add_error(
                None,
                "This account does not have a supported Student or Staff role.",
            )
        else:
            login(request, user)
            messages.success(request, f"Welcome back, {user.display_name}.")
            return redirect(destination)

    return render(
        request,
        "finder/login.html",
        {
            "form": form,
            "student_demo_accounts": STUDENT_ACCOUNTS,
            "staff_demo_accounts": STAFF_ACCOUNTS,
        },
    )


def logout_view(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    logout(request)
    messages.info(request, "You have been signed out securely.")
    return redirect("finder:login")


@role_required(STUDENT_ROLE)
def staff_directory(request):
    search_query = request.GET.get("q", "").strip()[:100]
    selected_interest = request.GET.get("interest", "").strip()[:80]

    interest_options = list(
        Interest.objects.order_by("name")
        .values_list("name", flat=True)
        .distinct()
    )
    normalised_options = {name.casefold(): name for name in interest_options}
    filter_error = ""

    profiles = (
        StaffProfile.objects.select_related("user")
        .prefetch_related("interests")
        .annotate(
            full_name=Concat(
                "user__first_name",
                Value(" "),
                "user__last_name",
            ),
            project_count=Count("project_ideas", distinct=True),
        )
    )

    if search_query:
        profiles = profiles.filter(
            Q(full_name__icontains=search_query)
            | Q(user__first_name__icontains=search_query)
            | Q(user__last_name__icontains=search_query)
        )

    if selected_interest:
        canonical_interest = normalised_options.get(selected_interest.casefold())
        if canonical_interest:
            selected_interest = canonical_interest
            profiles = profiles.filter(interests__name__iexact=canonical_interest)
        else:
            filter_error = "Choose an area of interest from the available options."
            selected_interest = ""

    profiles = profiles.distinct().order_by(
        "user__first_name",
        "user__last_name",
        "user__email",
    )

    return render(
        request,
        "finder/staff_directory.html",
        {
            "profiles": profiles,
            "result_count": profiles.count(),
            "interest_options": interest_options,
            "search_query": search_query,
            "selected_interest": selected_interest,
            "filter_error": filter_error,
        },
    )


@role_required(STUDENT_ROLE)
def staff_profile(request, profile_id):
    profile = get_object_or_404(
        StaffProfile.objects.select_related("user").prefetch_related(
            "interests",
            "project_ideas",
        ),
        pk=profile_id,
    )
    query = {
        key: value
        for key, value in {
            "q": request.GET.get("q", "").strip()[:100],
            "interest": request.GET.get("interest", "").strip()[:80],
        }.items()
        if value
    }
    back_url = reverse("finder:staff-directory")
    if query:
        back_url = f"{back_url}?{urlencode(query)}"

    return render(
        request,
        "finder/staff_profile.html",
        {"profile": profile, "back_url": back_url},
    )


@role_required(STAFF_ROLE)
def dashboard(request):
    profile = get_object_or_404(
        StaffProfile.objects.select_related("user").prefetch_related(
            "interests",
            "project_ideas",
        ),
        user=request.user,
    )
    return render(request, "finder/dashboard.html", {"profile": profile})


def _owned_staff_profile(request):
    return get_object_or_404(
        StaffProfile.objects.select_related("user"),
        user=request.user,
    )


@role_required(STAFF_ROLE)
@require_http_methods(["GET", "POST"])
def interest_create(request):
    profile = _owned_staff_profile(request)
    form = InterestForm(
        request.POST or None,
        staff_profile=profile,
    )
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            interest = form.save()
        messages.success(request, f"Added “{interest.name}” to your interests.")
        return redirect("finder:dashboard")
    return render(
        request,
        "finder/content_form.html",
        {
            "form": form,
            "eyebrow": "Profile expertise",
            "page_title": "Add an area of interest",
            "introduction": (
                "Add a concise subject area that helps students understand the "
                "projects you are prepared to supervise."
            ),
            "submit_label": "Add interest",
        },
    )


@role_required(STAFF_ROLE)
@require_http_methods(["GET", "POST"])
def interest_update(request, interest_id):
    profile = _owned_staff_profile(request)
    interest = get_object_or_404(
        Interest,
        pk=interest_id,
        staff_profile=profile,
    )
    form = InterestForm(
        request.POST or None,
        instance=interest,
        staff_profile=profile,
    )
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            updated_interest = form.save()
        messages.success(
            request,
            f"Updated your interest to “{updated_interest.name}”.",
        )
        return redirect("finder:dashboard")
    return render(
        request,
        "finder/content_form.html",
        {
            "form": form,
            "eyebrow": "Profile expertise",
            "page_title": "Edit area of interest",
            "introduction": (
                "Update this subject area. The change will be visible on your "
                "student-facing profile."
            ),
            "submit_label": "Save changes",
        },
    )


@role_required(STAFF_ROLE)
@require_http_methods(["GET", "POST"])
def interest_delete(request, interest_id):
    profile = _owned_staff_profile(request)
    interest = get_object_or_404(
        Interest,
        pk=interest_id,
        staff_profile=profile,
    )
    if request.method == "POST":
        name = interest.name
        with transaction.atomic():
            interest.delete()
        messages.success(request, f"Deleted the interest “{name}”.")
        return redirect("finder:dashboard")
    return render(
        request,
        "finder/confirm_delete.html",
        {
            "object_name": interest.name,
            "object_type": "area of interest",
        },
    )


@role_required(STAFF_ROLE)
@require_http_methods(["GET", "POST"])
def project_create(request):
    profile = _owned_staff_profile(request)
    form = ProjectIdeaForm(
        request.POST or None,
        staff_profile=profile,
    )
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            project = form.save()
        messages.success(request, f"Added the project idea “{project.title}”.")
        return redirect("finder:dashboard")
    return render(
        request,
        "finder/content_form.html",
        {
            "form": form,
            "eyebrow": "Project opportunities",
            "page_title": "Add a project idea",
            "introduction": (
                "Describe a focused project direction that a student can understand "
                "and discuss with you."
            ),
            "submit_label": "Add project idea",
        },
    )


@role_required(STAFF_ROLE)
@require_http_methods(["GET", "POST"])
def project_update(request, project_id):
    profile = _owned_staff_profile(request)
    project = get_object_or_404(
        ProjectIdea,
        pk=project_id,
        staff_profile=profile,
    )
    form = ProjectIdeaForm(
        request.POST or None,
        instance=project,
        staff_profile=profile,
    )
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            updated_project = form.save()
        messages.success(
            request,
            f"Updated the project idea “{updated_project.title}”.",
        )
        return redirect("finder:dashboard")
    return render(
        request,
        "finder/content_form.html",
        {
            "form": form,
            "eyebrow": "Project opportunities",
            "page_title": "Edit project idea",
            "introduction": (
                "Update the title or description. Saved changes will appear on "
                "your student-facing profile."
            ),
            "submit_label": "Save changes",
        },
    )


@role_required(STAFF_ROLE)
@require_http_methods(["GET", "POST"])
def project_delete(request, project_id):
    profile = _owned_staff_profile(request)
    project = get_object_or_404(
        ProjectIdea,
        pk=project_id,
        staff_profile=profile,
    )
    if request.method == "POST":
        title = project.title
        with transaction.atomic():
            project.delete()
        messages.success(request, f"Deleted the project idea “{title}”.")
        return redirect("finder:dashboard")
    return render(
        request,
        "finder/confirm_delete.html",
        {
            "object_name": project.title,
            "object_type": "project idea",
        },
    )
