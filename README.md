# Secure Sharing App

This is a FastAPI-based web application for secure file sharing and basic arithmetic operations. The project includes user registration, login with JWT token authentication, and file upload functionality.

## Features

### User Management:
- User registration with hashed password storage.
- JWT-based user authentication.

### File Upload:
- Upload and store files securely in a designated directory.

### Arithmetic Operations:
- Addition and multiplication of two numbers.

## Project Structure

```
.
├── app.py          # Main FastAPI application
├── models.py       # Pydantic models for user handling
├── utils.py        # Utility functions for password hashing and JWT
├── test_app.py     # Test cases using Pytest
├── requirements.txt # Project dependencies
├── README.md       # Project documentation
└── files/          # Directory to store uploaded files
```

## Installation

1. Clone the repository:
```bash
git clone <repository_url>
cd secure_sharing
```

2. Create a virtual environment:
```bash
python -m venv secure_sharing
```

3. Activate the virtual environment:

**On Windows:**
```bash
.\secure_sharing\Scripts\activate
```

**On Mac/Linux:**
```bash
source secure_sharing/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
uvicorn app:app --reload
```
The app will be accessible at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## API Endpoints

### Health Check
- `GET /` : Root endpoint
- `GET /health` : Check application health

### User Management
- `POST /users/` : Register a new user

Example Request Body:
```json
{
   "username": "test_user",
   "email": "user@example.com",
   "password": "password123"
}
```

- `POST /login/` : Login user and get JWT token

Example Request Body:
```json
{
   "username": "test_user",
   "password": "password123"
}
```

### File Upload
- `POST /uploadfile/` : Upload a file
  - Form Data: `file`

### Arithmetic Operations
- `GET /add/{a}/{b}` : Add two numbers
- `GET /multiply/{a}/{b}` : Multiply two numbers

## Running Tests
Pytest is used for testing the application:
```bash
pytest test_app.py
