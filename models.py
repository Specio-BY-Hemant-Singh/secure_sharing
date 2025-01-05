from pydantic import BaseModel

# Model for creating a user
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# Model for user login
class UserLogin(BaseModel):
    username: str
    password: str
