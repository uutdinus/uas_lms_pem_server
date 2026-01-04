from ninja.errors import HttpError

def allow_roles(*roles):
    def checker(request):
        user = request.user
        if not user:
            raise HttpError(401, "Unauthorized")

        if user.role not in roles:
            raise HttpError(403, "Forbidden: insufficient role")

        return True
    return checker
