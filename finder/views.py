from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth import login, logout
from django.db.models import Count, Q, Value
from django.db.models.functions import Concat
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .access import STAFF_ROLE, STUDENT_ROLE, has_role, role_for, role_required
from .forms import EmailAuthenticationForm
from .models import Interest, StaffProfile


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

    return render(request, "finder/login.html", {"form": form})


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
