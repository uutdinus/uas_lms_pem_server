from ninja import Router
from ninja.security import HttpBearer
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from ninja.errors import HttpError

from .models import User, Course, Lesson, Assignment, Submission
from .schemas import (
    UserSchema,
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
        user = request.user
        if not user:
            raise HttpError(401, "Unauthorized")

        if user.role not in roles:
            raise HttpError(403, "Forbidden: insufficient role")

        return True
    return checker


# ======================
# AUTH / LOGIN (JWT)
# ======================
@router.post("/login")
def login(request, username: str, password: str):
    user = authenticate(username=username, password=password)
    if not user:
        return {"error": "Invalid username or password"}

    token = create_token(user)
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
    }


# ======================
# USERS (ADMIN ONLY)
# ======================
@router.get("/users", response=list[UserSchema], auth=JWTAuth())
def list_users(request):
    allow_roles("admin")(request)
    return User.objects.all()


# ======================
# COURSES
# ======================
@router.get("/courses", response=list[CourseSchema])
def list_courses(request):
    return Course.objects.all()


@router.post("/courses", response=CourseSchema, auth=JWTAuth())
def create_course(request, data: CourseCreateSchema):
    allow_roles("admin", "dosen")(request)

    instructor = get_object_or_404(User, id=data.instructor_id)
    return Course.objects.create(
        title=data.title,
        description=data.description,
        instructor=instructor
    )


# ======================
# LESSONS
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
# ASSIGNMENTS
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
# SUBMISSIONS
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

    return Submission.objects.create(
        answer=data.answer,
        student=student,
        assignment=assignment
    )
