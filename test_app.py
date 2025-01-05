import pytest
from fastapi.testclient import TestClient
from app import app

# Initialize the TestClient with the FastAPI app
client = TestClient(app)

# Test the root endpoint
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Secure Sharing App!"}

# Test the health check route
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}

# Test user creation
def test_create_user():
    # Create a sample user data to test the user creation
    user_data = {
        "username": "test_user",
        "email": "test_user@example.com",
        "password": "testpassword"
    }
    
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json() == {"message": "User test_user created successfully!"}

# Test user login with correct credentials
def test_login_user():
    # Create a login payload for a test user
    login_data = {
        "username": "test_user",
        "password": "testpassword"
    }
    
    response = client.post("/login/", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["message"] == "User test_user logged in successfully!"

# Test user login with incorrect credentials
def test_login_invalid_user():
    login_data = {
        "username": "test_user",
        "password": "wrongpassword"
    }
    
    response = client.post("/login/", json=login_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid credentials"}

# Test the file upload functionality
def test_upload_file():
    # Simulate file upload using TestClient's `files` parameter
    with open("testfile.txt", "w") as f:
        f.write("This is a test file content.")
    
    with open("testfile.txt", "rb") as file:
        response = client.post("/uploadfile/", files={"file": ("testfile.txt", file, "text/plain")})
    
    assert response.status_code == 200
    assert "info" in response.json()
    assert "saved at" in response.json()["info"]

# Test simple addition
def test_addition():
    response = client.get("/add/3/5")
    assert response.status_code == 200
    assert response.json() == {"result": 8}

# Test simple multiplication
def test_multiplication():
    response = client.get("/multiply/3/5")
    assert response.status_code == 200
    assert response.json() == {"result": 15}
