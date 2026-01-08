from ninja import Schema
from datetime import datetime
from typing import Optional


class UserSchema(Schema):
    id: int
    username: str
    email: str
    role: str


# ✅ WAJIB UAS: Register user
class RegisterSchema(Schema):
    username: str
    password: str
    email: Optional[str] = None
    role: str = "mahasiswa"


class CourseSchema(Schema):
    id: int
    title: str
    description: str
    instructor_id: int
    # ✅ WAJIB UAS: created_at
    created_at: datetime


class CourseCreateSchema(Schema):
    title: str
    description: str
    instructor_id: int


class LessonSchema(Schema):
    id: int
    title: str
    content: str
    course_id: int


class LessonCreateSchema(Schema):
    title: str
    content: str
    course_id: int


class AssignmentSchema(Schema):
    id: int
    title: str
    deadline: datetime
    course_id: int


class AssignmentCreateSchema(Schema):
    title: str
    deadline: datetime
    course_id: int


class SubmissionSchema(Schema):
    id: int
    answer: str
    grade: int | None
    student_id: int
    assignment_id: int
    
    file: Optional[str] = None


class SubmissionCreateSchema(Schema):
    answer: str
    student_id: int
    assignment_id: int
    # optional: kalau nanti kamu bikin endpoint upload, field ini bisa dipakai sebagai path
    file: Optional[str] = None
