import jwt
from datetime import datetime, timedelta
from django.conf import settings
from ninja.security import HttpBearer
from django.contrib.auth import authenticate
from .models import User

JWT_SECRET = settings.SECRET_KEY
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 60


def create_token(user: User):
    payload = {
        "user_id": user.id,
        "username": user.username,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(
                token, JWT_SECRET, algorithms=[JWT_ALGORITHM]
            )
            user = User.objects.get(id=payload["user_id"])
            request.user = user
            return user
        except Exception:
            return None
