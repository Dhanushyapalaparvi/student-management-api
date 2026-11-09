
from uuid import uuid4


def create_test_student(client, email, name="Test Student"):

    response = client.post(
        "/students",
        json={
            "name": name,
            "email": email,
            "age": 21,
            "department": "Computer Science",
        },
    )

    assert response.status_code == 201

    return response.json()


def test_root_endpoint(client):

    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Welcome to the Student Management API",
        "status": "running",
    }


def test_health_endpoint(client):

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy",
    }


def test_unknown_endpoint(client):

    response = client.get("/unknown")

    assert response.status_code == 404


def test_create_student_with_invalid_age(client):

    response = client.post(
        "/students",
        json={
            "name": "Rahul Sharma",
            "email": "rahul@example.com",
            "age": 15,
            "department": "Computer Science",
        },
    )

    assert response.status_code == 422


def test_create_student_with_invalid_email(client):

    response = client.post(
        "/students",
        json={
            "name": "Rahul Sharma",
            "email": "not-an-email",
            "age": 20,
            "department": "Computer Science",
        },
    )

    assert response.status_code == 422


def test_create_duplicate_email(client):

    email = f"duplicate-{uuid4().hex}@example.com"

    create_test_student(client, email)

    response = client.post(
        "/students",
        json={
            "name": "Another Student",
            "email": email,
            "age": 22,
            "department": "IT",
        },
    )

    assert response.status_code == 409

    assert response.json() == {
        "detail": "A student with this email already exists"
    }


def test_update_student_with_duplicate_email(client):

    student1 = create_test_student(
        client,
        f"rahul-{uuid4().hex}@example.com",
        "Rahul",
    )

    student2 = create_test_student(
        client,
        f"priya-{uuid4().hex}@example.com",
        "Priya",
    )

    response = client.put(
        f"/students/{student1['id']}",
        json={
            "name": "Rahul Updated",
            "email": student2["email"],
            "age": 23,
            "department": "IT",
        },
    )

    assert response.status_code == 409

    verification = client.get(
        f"/students/{student1['id']}"
    )

    assert verification.status_code == 200

    assert verification.json()["email"] == student1["email"]


def test_patch_student_with_duplicate_email(client):

    student1 = create_test_student(
        client,
        f"arjun-{uuid4().hex}@example.com",
        "Arjun",
    )

    student2 = create_test_student(
        client,
        f"rohan-{uuid4().hex}@example.com",
        "Rohan",
    )

    response = client.patch(
        f"/students/{student1['id']}",
        json={
            "email": student2["email"]
        },
    )

    assert response.status_code == 409

    verification = client.get(
        f"/students/{student1['id']}"
    )

    assert verification.status_code == 200

    assert verification.json()["email"] == student1["email"]


def test_get_student_by_id(client):

    student = create_test_student(
        client,
        f"student-{uuid4().hex}@example.com",
    )

    response = client.get(
        f"/students/{student['id']}"
    )

    assert response.status_code == 200

    assert response.json()["id"] == student["id"]


def test_get_nonexistent_student(client):

    response = client.get("/students/99999")

    assert response.status_code == 404
