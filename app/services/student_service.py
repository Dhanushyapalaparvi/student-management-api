
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Student
from app.schemas.student import (
    StudentCreate,
    StudentUpdate,
)


class DuplicateStudentEmailError(Exception):
    """Raised when a student email already exists."""


def commit_or_handle_integrity_error(db: Session) -> None:
    try:
        db.commit()

    except IntegrityError as exc:
        db.rollback()

        original_error = str(exc.orig).lower()

        is_duplicate_email = any(
            error in original_error
            for error in [
                "students.email",
                "students_email_key",
                "ix_students_email",
            ]
        )

        if is_duplicate_email:
            raise DuplicateStudentEmailError(
                "A student with this email already exists"
            ) from exc

        raise


def create_student(
    db: Session,
    student_data: StudentCreate,
) -> Student:

    new_student = Student(
        name=student_data.name,
        email=str(student_data.email),
        age=student_data.age,
        department=student_data.department,
    )

    db.add(new_student)

    commit_or_handle_integrity_error(db)

    db.refresh(new_student)

    return new_student


def get_students(
    db: Session,
    skip: int,
    limit: int,
    department: str | None,
) -> list[Student]:

    statement = select(Student)

    if department:
        statement = statement.where(
            Student.department == department
        )

    statement = (
        statement
        .order_by(Student.id)
        .offset(skip)
        .limit(limit)
    )

    students = db.scalars(statement).all()

    return list(students)


def get_student(
    db: Session,
    student_id: int,
) -> Student | None:

    return db.get(Student, student_id)


def update_student(
    db: Session,
    student_id: int,
    student_data: StudentUpdate,
) -> Student | None:

    student = db.get(Student, student_id)

    if student is None:
        return None

    student.name = student_data.name
    student.email = str(student_data.email)
    student.age = student_data.age
    student.department = student_data.department

    commit_or_handle_integrity_error(db)

    db.refresh(student)

    return student


def patch_student(
    db: Session,
    student_id: int,
    update_data: dict,
) -> Student | None:

    student = db.get(Student, student_id)

    if student is None:
        return None

    for field, value in update_data.items():

        if field == "email":
            value = str(value)

        setattr(student, field, value)

    commit_or_handle_integrity_error(db)

    db.refresh(student)

    return student


def delete_student(
    db: Session,
    student_id: int,
) -> bool:

    student = db.get(Student, student_id)

    if student is None:
        return False

    db.delete(student)
    db.commit()

    return True
