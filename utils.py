from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

# Set up password context (using bcrypt for hashing passwords)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key for JWT encoding/decoding
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Function to hash a password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Function to verify a password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Function to create a JWT token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to verify the JWT token (for authentication)
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
