from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied


STUDENT_ROLE = "Student"
STAFF_ROLE = "Staff"


def has_role(user, role):
    return user.is_authenticated and user.groups.filter(name=role).exists()


def role_for(user):
    if has_role(user, STUDENT_ROLE):
        return STUDENT_ROLE
    if has_role(user, STAFF_ROLE):
        return STAFF_ROLE
    return None


def role_required(role):
    """Require authentication and enforce a role on the server."""

    def decorator(view_function):
        @wraps(view_function)
        def wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if not has_role(request.user, role):
                raise PermissionDenied
            return view_function(request, *args, **kwargs)

        return wrapped

    return decorator
