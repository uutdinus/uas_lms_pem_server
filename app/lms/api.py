from ninja import Router
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from ninja.errors import HttpError
from django.core.cache import cache

from .models import User, Course, Lesson, Assignment, Submission
from .schemas import (
    UserSchema,
    RegisterSchema,
    CourseSchema, CourseCreateSchema,
    LessonSchema, LessonCreateSchema,
    AssignmentSchema, AssignmentCreateSchema,
    SubmissionSchema, SubmissionCreateSchema
)
from .auth import create_token, JWTAuth

router = Router()

# ======================
# RBAC HELPER
# ======================
def allow_roles(*roles):
    def checker(request):
        user = getattr(request, "user", None)
        if not user:
            raise HttpError(401, "Unauthorized")
        if user.role not in roles:
            raise HttpError(403, "Forbidden: insufficient role")
        return True
    return checker


# ======================
# RATE LIMITING (LOGIN) - WAJIB UAS
# ======================
LOGIN_RL_MAX = 5
LOGIN_RL_WINDOW = 60  # detik

def _client_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


# ======================
# AUTH - REGISTER (WAJIB UAS)
# ======================
@router.post("/register", response=UserSchema)
def register(request, data: RegisterSchema):
    if data.role not in ("admin", "dosen", "mahasiswa"):
        raise HttpError(400, "Invalid role")

    if User.objects.filter(username=data.username).exists():
        raise HttpError(400, "Username already exists")

    user = User.objects.create_user(
        username=data.username,
        password=data.password,
        email=data.email or "",
        role=data.role,
    )
    return user


# ======================
# AUTH - LOGIN (JWT) + RATE LIMIT (WAJIB UAS)
# ======================
@router.post("/login")
def login(request, username: str, password: str):
    ip = _client_ip(request)
    key = f"rl:login:{ip}"

    attempts = cache.get(key, 0)
    if attempts >= LOGIN_RL_MAX:
        raise HttpError(429, "Too many login attempts. Try again later.")

    user = authenticate(username=username, password=password)
    if not user:
        cache.set(key, attempts + 1, LOGIN_RL_WINDOW)
        raise HttpError(401, "Invalid username or password")

    cache.delete(key)

    token = create_token(user)  # pastikan token punya exp di auth.py
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
    }


# ======================
# USERS (ADMIN ONLY) - optional
# ======================
@router.get("/users", response=list[UserSchema], auth=JWTAuth())
def list_users(request):
    allow_roles("admin")(request)
    return User.objects.all()


# ======================
# REDIS CACHE (WAJIB UAS) untuk GET /courses
# ======================
COURSE_CACHE_KEY = "cache:lms:courses"
COURSE_CACHE_TTL = 60  # detik


# ======================
# COURSES (WAJIB UAS)
# - GET /courses (protected + RBAC)
# - POST /courses (protected)
# - DELETE /courses/{id} (protected)
# - caching + invalidation
# ======================
@router.get("/courses", response=list[CourseSchema], auth=JWTAuth())
def list_courses(request):
    # Mahasiswa hanya GET course, admin/dosen juga boleh GET
    allow_roles("admin", "dosen", "mahasiswa")(request)

    cached = cache.get(COURSE_CACHE_KEY)
    if cached is not None:
        return cached

    qs = Course.objects.all().order_by("-id")
    data = [
        {
            "id": c.id,
            "title": c.title,
            "description": c.description,
            "instructor_id": c.instructor_id,
            "created_at": c.created_at,
        }
        for c in qs
    ]
    cache.set(COURSE_CACHE_KEY, data, COURSE_CACHE_TTL)
    return data


@router.post("/courses", response=CourseSchema, auth=JWTAuth())
def create_course(request, data: CourseCreateSchema):
    allow_roles("admin", "dosen")(request)

    instructor = get_object_or_404(User, id=data.instructor_id)
    course = Course.objects.create(
        title=data.title,
        description=data.description,
        instructor=instructor
    )

    # cache invalidation (WAJIB UAS)
    cache.delete(COURSE_CACHE_KEY)
    return course


@router.delete("/courses/{course_id}", auth=JWTAuth())
def delete_course(request, course_id: int):
    allow_roles("admin", "dosen")(request)

    course = get_object_or_404(Course, id=course_id)
    course.delete()

    # cache invalidation (WAJIB UAS)
    cache.delete(COURSE_CACHE_KEY)
    return {"message": "Course deleted"}


# ======================
# REDIS SESSION TEST (WAJIB UAS)
# ======================
@router.get("/test-session", auth=JWTAuth())
def test_session(request):
    allow_roles("admin", "dosen", "mahasiswa")(request)

    count = request.session.get("count", 0)
    count += 1
    request.session["count"] = count

    return {
        "message": "Session stored in Redis (via cache backend).",
        "session_key": request.session.session_key,
        "count": count,
        "user": request.user.username,
        "role": request.user.role,
    }


# ======================
# LESSONS (optional untuk UAS, tapi aman dibiarkan)
# ======================
@router.get("/lessons", response=list[LessonSchema])
def list_lessons(request):
    return Lesson.objects.all()


@router.post("/lessons", response=LessonSchema, auth=JWTAuth())
def create_lesson(request, data: LessonCreateSchema):
    allow_roles("admin", "dosen")(request)

    course = get_object_or_404(Course, id=data.course_id)
    return Lesson.objects.create(
        title=data.title,
        content=data.content,
        course=course
    )


# ======================
# ASSIGNMENTS (optional untuk UAS, tapi aman dibiarkan)
# ======================
@router.get("/assignments", response=list[AssignmentSchema])
def list_assignments(request):
    return Assignment.objects.all()


@router.post("/assignments", response=AssignmentSchema, auth=JWTAuth())
def create_assignment(request, data: AssignmentCreateSchema):
    allow_roles("admin", "dosen")(request)

    course = get_object_or_404(Course, id=data.course_id)
    return Assignment.objects.create(
        title=data.title,
        deadline=data.deadline,
        course=course
    )


# ======================
# SUBMISSIONS (optional untuk UAS, tapi aman)
# ======================
@router.get("/submissions", response=list[SubmissionSchema], auth=JWTAuth())
def list_submissions(request):
    allow_roles("admin", "dosen")(request)
    return Submission.objects.all()


@router.post("/submissions", response=SubmissionSchema, auth=JWTAuth())
def create_submission(request, data: SubmissionCreateSchema):
    allow_roles("mahasiswa")(request)

    student = get_object_or_404(User, id=data.student_id)
    assignment = get_object_or_404(Assignment, id=data.assignment_id)

    submission = Submission.objects.create(
        answer=data.answer,
        student=student,
        assignment=assignment
    )

    # kalau kamu ingin isi field file lewat path (opsional)
    if getattr(data, "file", None):
        submission.file = data.file  # biasanya untuk upload harus pakai endpoint upload, tapi ini opsional
        submission.save()

    return submission
