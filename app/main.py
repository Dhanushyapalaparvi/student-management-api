

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


from app.routers.students import router as student_router
from app.services.student_service import DuplicateStudentEmailError




app = FastAPI(
    title="Student Management API",
    description="An API to manage students, courses, marks, and results.",
    version="1.0.0",
)


@app.exception_handler(DuplicateStudentEmailError)
async def duplicate_student_email_handler(
    request: Request,
    exc: DuplicateStudentEmailError,
):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )


app.include_router(student_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to the Student Management API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
