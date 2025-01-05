# Secure File Sharing System

This project implements a secure file-sharing system using Flask, SQLAlchemy, and JWT for user authentication and file management. The system allows two types of users: **Ops Users** and **Client Users**. Ops users can upload files, while client users can sign up, verify their email, and download files securely.

## Features

- **Ops User:**
  - Can upload files (`pptx`, `docx`, `xlsx`) securely.
  - File uploads are restricted to specific file types.
- **Client User:**
  - Can sign up and receive a verification email.
  - Can log in only after email verification.
  - Can list and download files securely using a tokenized URL.
- **Security:**
  - JWT-based authentication for secure API access.
  - Tokenized download URLs for secure file downloads, which are validated for the correct user.

## Technologies Used

- **Flask:** A lightweight WSGI web application framework.
- **Flask-SQLAlchemy:** For database interaction.
- **Flask-JWT-Extended:** For user authentication via JWT tokens.
- **Flask-Mail:** To send verification emails.
- **Flask-Uploads:** To handle file uploads.
- **SQLite:** A lightweight relational database used for development (replaceable with other databases).
- **Werkzeug:** For secure file handling.

## Installation

### Clone the Repository
```
git clone https://github.com/Specio-BY-Hemant-Singh/secure_sharing.git
cd secure-file-sharing
```

### 2. Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///path_to_your_database.db
JWT_SECRET_KEY=your_jwt_secret_key
MAIL_SERVER=smtp.yourmailserver.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_email_password
```

### 5. Initialize the Database
```
python app.py
```

### 6. Run the Application
```
python app.py
```

## API Endpoints

### User Operations
- `POST /signup`: Create a new user and send a verification email.
- `GET /verify/<token>`: Verify the user’s email using the token received in the verification email.
- `POST /login`: Log in the user and return a JWT access token.
- `GET /user`: Retrieve the current user’s information (requires JWT authentication).

### File Operations (For Ops Users Only)
- `POST /files`: Upload a file (only pptx, docx, xlsx).
- `GET /files`: List all files uploaded by the authenticated Ops user.

### File Download (For Client Users Only)
- `GET /download-file/<file_id>`: Generate a secure download link for a file.
- `GET /download/<file_id>/<token>`: Download the file securely using the generated download token.

### File Upload Restrictions
- Ops users can upload files of type pptx, docx, and xlsx only.
- Files are saved securely and are only accessible by the user who uploaded them.

### Testing
You can use tools like Postman or cURL to test the APIs.
