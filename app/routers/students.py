
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.student import (
    StudentCreate,
    StudentResponse,
    StudentUpdate,
    StudentPatch,
)
from app.services import student_service


router = APIRouter(
    prefix="/students",
    tags=["Students"],
)


@router.post(
    "",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
):
    return student_service.create_student(db, student)


@router.get(
    "",
    response_model=list[StudentResponse],
)
def get_students(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    department: str | None = Query(default=None, min_length=2),
    db: Session = Depends(get_db),
):
    return student_service.get_students(
        db,
        skip,
        limit,
        department,
    )


@router.get(
    "/{student_id}",
    response_model=StudentResponse,
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
):
    student = student_service.get_student(db, student_id)

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found",
        )

    return student


@router.put(
    "/{student_id}",
    response_model=StudentResponse,
)
def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db),
):
    student = student_service.update_student(
        db,
        student_id,
        student_data,
    )

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found",
        )

    return student


@router.patch(
    "/{student_id}",
    response_model=StudentResponse,
)
def patch_student(
    student_id: int,
    student_data: StudentPatch,
    db: Session = Depends(get_db),
):
    update_data = student_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="At least one field must be provided",
        )

    if any(value is None for value in update_data.values()):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Fields cannot be null",
        )

    student = student_service.patch_student(
        db,
        student_id,
        update_data,
    )

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found",
        )

    return student


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
):
    deleted = student_service.delete_student(db, student_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with ID {student_id} not found",
        )

    return None
