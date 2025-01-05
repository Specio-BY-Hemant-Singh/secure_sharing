
from app import app, db
from models import User, File
from flask_jwt_extended import create_access_token
import pytest

if __name__ == '__main__':
    pytest.main([__file__])
data = {
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "password123"
}

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
    client = app.test_client()
    yield client
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def ops_user():
    user = User(username="ops_user", email="ops@example.com", is_ops_user=True)
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def client_user():
    user = User(username="client_user", email="client@example.com")
    user.set_password("password123")
    user.email_verified = True
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def access_token(client_user):
    return create_access_token(identity=client_user.id)

# Test User Registration
def test_signup(client):
    response = client.post('/signup', json=data)
    assert response.status_code == 201
    assert b"User created successfully" in response.data

# Test User Login
def test_login(client, client_user):
    response = client.post('/login', json={
        "username": client_user.username,
        "password": "password123"
    })
    assert response.status_code == 200
    assert 'access_token' in response.get_json()

# Test Unauthorized File Upload
def test_upload_file_unauthorized(client, access_token):
    response = client.post('/files', headers={
        'Authorization': f'Bearer {access_token}'
    }, data={
        'file': (open('tests/sample.docx', 'rb'), 'sample.docx')
    })
    assert response.status_code == 403
    assert b"Only Ops users can upload files" in response.data

# Test Authorized File Upload
def test_upload_file_authorized(client, ops_user):
    token = create_access_token(identity=ops_user.id)
    response = client.post('/files', headers={
        'Authorization': f'Bearer {token}'
    }, data={
        'file': (open('tests/sample.docx', 'rb'), 'sample.docx')
    })
    assert response.status_code == 201

# Test File Listing
def test_list_files(client, access_token):
    response = client.get('/files', headers={
        'Authorization': f'Bearer {access_token}'
    })
    assert response.status_code == 200

# Test Secure File Download Link Generation
def test_download_file_link(client, ops_user):
    token = create_access_token(identity=ops_user.id)
    file = File(filename="sample.docx", user_id=ops_user.id)
    db.session.add(file)
    db.session.commit()

    response = client.get(f'/download-file/{file.id}', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    assert 'download-link' in response.get_json()

# Test Secure File Download
def test_secure_file_download(client, ops_user):
    token = create_access_token(identity=ops_user.id)
    file = File(filename="sample.docx", user_id=ops_user.id)
    file.download_token = "valid_token"
    db.session.add(file)
    db.session.commit()

    response = client.get(f'/download/{file.id}/valid_token')
    assert response.status_code == 200
    assert b"PK" in response.data  # Checking for binary file content marker

# Test Invalid Download Token
def test_invalid_download_token(client):
    response = client.get('/download/1/invalid_token')
    assert response.status_code == 403
    assert b"Invalid download token" in response.data

