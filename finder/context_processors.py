from .access import role_for


def user_role(request):
    return {"current_role": role_for(request.user)}
