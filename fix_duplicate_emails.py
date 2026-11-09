from sqlalchemy import select

from app.db.session import SessionLocal
from app.models import Student


def fix_duplicate_email():
    with SessionLocal() as db:
        student = db.get(Student, 4)

        if student is None:
            print("Student not found.")
            return

        student.email = "rahul.test2@example.com"

        db.commit()

        print("Email updated successfully.")


if __name__ == "__main__":
    fix_duplicate_email()