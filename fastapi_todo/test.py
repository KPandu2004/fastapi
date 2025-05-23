from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_student_success():
    response = client.post("/students",json={
        "name":"Alice",
        "age":22,
        "grade":"A"
    })
    assert response.status_code == 201
    assert response.json()["message"] == "Student added successfully"

def test_get_all_students():
    response = client.get("/students")
    print("Status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 200
    assert "data" in response.json()

def test_partial_update_student_success():
    response=client.patch("/students/0",json={
        "age":22
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Student updated successfully"
    assert response.json()["data"]["age"] == 22
    print("Status code:", response.status_code)
    print("Response JSON:", response.json())

def test_partial_update_invalid_id():
    response=client.patch("/students/999", json={"age":30})
    assert response.status_code == 404
    assert "Student with ID" in response.json()["message"]
    print("Status code:", response.status_code)

def test_create_student_invalid_data():
    response = client.post("/students",json={
        "name":"Bob",
    })
    assert response.status_code == 422
    print("Status code:", response.status_code)
    print("Response JSON:", response.json())

def test_patch_student_invalid_data():
    response = client.patch("/students/0",json={
        "age":"twenty"
    })
    assert response.status_code == 422
    print("Status code:", response.status_code)
    print("Response JSON:", response.json())