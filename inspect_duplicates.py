from sqlalchemy import select

from app.db.session import SessionLocal
from app.models import Student


def inspect_duplicates():
    with SessionLocal() as db:
        statement = (
            select(Student)
            .where(Student.email == "rahul@example.com")
            .order_by(Student.id)
        )

        students = db.scalars(statement).all()

        for student in students:
            print("-" * 40)
            print(f"ID: {student.id}")
            print(f"Name: {student.name}")
            print(f"Email: {student.email}")
            print(f"Age: {student.age}")
            print(f"Department: {student.department}")


if __name__ == "__main__":
    inspect_duplicates()