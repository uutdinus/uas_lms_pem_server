import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
from ninja.security import HttpBearer
from ninja.errors import HttpError
from .models import User

JWT_SECRET = settings.SECRET_KEY
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 60


def create_token(user: User):
    now = datetime.now(timezone.utc)
    payload = {
        "user_id": user.id,
        "username": user.username,
        "role": user.role,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=JWT_EXPIRE_MINUTES)).timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            user = User.objects.get(id=payload["user_id"])
            request.user = user
            return user

        except jwt.ExpiredSignatureError:
            # ✅ WAJIB UAS: token expired tidak bisa dipakai
            raise HttpError(401, "Token expired")

        except (jwt.InvalidTokenError, User.DoesNotExist, KeyError):
            raise HttpError(401, "Invalid token")
