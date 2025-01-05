from fastapi import FastAPI, HTTPException, File, UploadFile
from models import UserCreate, UserLogin
from utils import hash_password, verify_password, create_access_token
import os
from utils import hash_password


app = FastAPI()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Secure Sharing App!"}

# Health check route
@app.get("/health")
def health_check():
    return {"status": "OK"}

# Route to create a new user
@app.post("/users/")
def create_user(user: UserCreate):
    # Here, simulate saving the user data (you should connect to a database in a real app)
    hashed_password = hash_password(user.password)
    # Simulate saving the user with hashed password (in actual app, save it to the database)
    return {"message": f"User {user.username} created successfully!"}

# Generate a properly hashed password for testing
hashed_password = hash_password("testpassword")
# Route to handle user login
@app.post("/login/")
def login_user(user: UserLogin):
    if user.username == "test_user" and verify_password(user.password, hashed_password):
        token = create_access_token(data={"sub": user.username})
        return {"message": f"User {user.username} logged in successfully!", "access_token": token}
    else:
        raise HTTPException(status_code=400, detail="Invalid credentials")

# Route to upload a file
@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    # Ensure the 'files' directory exists
    os.makedirs("files", exist_ok=True)
    
    file_location = f"files/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    
    return {"info": f"File '{file.filename}' saved at '{file_location}'"}

# Simple route for addition
@app.get("/add/{a}/{b}")
def add(a: int, b: int):
    return {"result": a + b}

# Simple route for multiplication
@app.get("/multiply/{a}/{b}")
def multiply(a: int, b: int):
    return {"result": a * b}
