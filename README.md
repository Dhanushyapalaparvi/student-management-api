# Student Management API

A RESTful Student Management API built using **FastAPI, SQLAlchemy, and SQLite**. This project provides endpoints to create, retrieve, update, and delete student records, with input validation, database migrations, duplicate email protection, and automated testing.

## Features

- **Student CRUD Operations:** Create, retrieve, update, partially update, and delete student records.
- **Data Validation:** Request validation using Pydantic.
- **Email Validation:** Validates email addresses and prevents duplicate student emails.
- **Database Integration:** Persistent data storage using SQLite and SQLAlchemy ORM.
- **Database Migrations:** Schema version control using Alembic.
- **Error Handling:** Appropriate HTTP status codes and meaningful error responses.
- **Pagination:** Supports `skip` and `limit` query parameters when retrieving students.
- **Filtering:** Filter student records by department.
- **Automated Testing:** Endpoint and validation tests using Pytest.
- **Health Check:** Dedicated endpoint to verify API availability.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| FastAPI | REST API framework |
| SQLAlchemy | ORM and database operations |
| SQLite | Relational database |
| Pydantic | Data validation and serialization |
| Alembic | Database migrations |
| Pytest | Automated testing |
| Uvicorn | ASGI server |

## Project Structure

```text
student-management-api/
│
├── alembic/
│   ├── versions/
│   │   └── fed75aabce72_add_unique_student_email.py
│   ├── env.py
│   ├── README
│   └── script.py.mako
│
├── app/
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── session.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── student.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   └── students.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── student.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── student_service.py
│   │
│   └── main.py
│
├── tests/
│   ├── conftest.py
│   └── test_main.py
│
├── .gitignore
├── alembic.ini
├── check_duplicate_emails.py
├── fix_duplicate_emails.py
└── inspect_duplicates.py
```

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Dhanushyapalaparvi/student-management-api.git
```

Navigate into the project directory:

```bash
cd student-management-api
```

### 2. Create a Virtual Environment

```bash
python -m venv studentenv
```

Activate it on Windows PowerShell:

```powershell
.\studentenv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install fastapi "uvicorn[standard]" sqlalchemy alembic "pydantic[email]" pytest httpx
```

### 4. Apply Database Migrations

```bash
python -m alembic upgrade head
```

This applies the available database migration and creates the unique email index.

### 5. Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically generates interactive API documentation.

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

## API Endpoints

### General Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |

### Student Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/students` | Create a student |
| GET | `/students` | Retrieve all students |
| GET | `/students/{student_id}` | Retrieve a student by ID |
| PUT | `/students/{student_id}` | Fully update a student |
| PATCH | `/students/{student_id}` | Partially update a student |
| DELETE | `/students/{student_id}` | Delete a student |

### Query Parameters

The `GET /students` endpoint supports:

| Parameter | Default | Description |
|---|---|---|
| `skip` | 0 | Number of records to skip |
| `limit` | 10 | Maximum number of records (1–100) |
| `department` | None | Filter students by department |

Example:

```text
GET /students?skip=0&limit=5&department=CSE
```

## Request Example

### Create a Student

**POST** `/students`

Request body:

```json
{
    "name": "Rahul Sharma",
    "email": "rahul@example.com",
    "age": 20,
    "department": "Computer Science"
}
```

Successful response: `201 Created`

```json
{
    "id": 1,
    "name": "Rahul Sharma",
    "email": "rahul@example.com",
    "age": 20,
    "department": "Computer Science"
}
```

### Update a Student

**PUT** `/students/1`

All student fields must be provided.

### Partially Update a Student

**PATCH** `/students/1`

Only the fields that need modification are required.

Example:

```json
{
    "department": "Information Technology"
}
```

## Validation and Error Handling

The API implements request validation and handles common errors using appropriate HTTP status codes.

| Status Code | Description |
|---|---|
| 200 | Successful request |
| 201 | Student successfully created |
| 204 | Student successfully deleted |
| 404 | Student not found |
| 409 | Duplicate student email |
| 422 | Request validation error |

### Implemented Validation Rules

- Student name must contain 2–100 characters.
- Email must have a valid email format.
- Student age must be between 16 and 100.
- Department must contain 2–100 characters.
- Student email addresses must be unique.
- PATCH requests must contain at least one field.
- PATCH requests cannot explicitly set fields to null.

Duplicate email errors are handled using SQLAlchemy's `IntegrityError`, database rollback, and a custom exception handler to return `409 Conflict` instead of an internal server error.

## Database Migrations

This project uses Alembic to manage database schema changes.

Useful commands:

Check the current migration:

```bash
python -m alembic current
```

View migration history:

```bash
python -m alembic history
```

Apply migrations:

```bash
python -m alembic upgrade head
```

Generate a new migration:

```bash
python -m alembic revision --autogenerate -m "migration description"
```

## Running Tests

The project uses Pytest for automated testing.

Run all tests:

```bash
python -m pytest -v
```

The existing test suite covers:

- Root and health-check endpoints.
- Invalid endpoint handling.
- Student creation.
- Input validation.
- Duplicate email handling.
- Student update operations.

## Database

The application uses SQLite for persistent data storage.

Database file:

```text
student_management.db
```

SQLAlchemy manages database interactions, while Alembic tracks schema changes through migration scripts.

## Author

**Dhanush Yapalaparvi**

GitHub: [@Dhanushyapalaparvi](https://github.com/Dhanushyapalaparvi)

## License

This project is available under the MIT License.
