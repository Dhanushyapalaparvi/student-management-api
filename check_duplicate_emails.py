from sqlalchemy import func, select

from app.db.session import SessionLocal
from app.models import Student


def check_duplicate_emails():
    with SessionLocal() as db:
        statement = (
            select(
                Student.email,
                func.count(Student.id).label("count"),
            )
            .group_by(Student.email)
            .having(func.count(Student.id) > 1)
        )

        duplicates = db.execute(statement).all()

        if duplicates:
            print("Duplicate emails found:")
            for email, count in duplicates:
                print(f"{email}: {count} records")
        else:
            print("No duplicate emails found.")

        total_students = db.scalar(
            select(func.count()).select_from(Student)
        )

        print(f"Total students: {total_students}")


if __name__ == "__main__":
    check_duplicate_emails()