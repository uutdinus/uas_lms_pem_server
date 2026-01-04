from ninja import Schema
from datetime import datetime


class UserSchema(Schema):
    id: int
    username: str
    email: str
    role: str


class CourseSchema(Schema):
    id: int
    title: str
    description: str
    instructor_id: int


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


class SubmissionCreateSchema(Schema):
    answer: str
    student_id: int
    assignment_id: int
