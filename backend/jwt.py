import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from datetime import datetime,timedelta,timezone
from jose import jwt
from .models import UserLoginSignUp

load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

my_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password:str):
    return my_context.hash(password)

def verify_password(hashed_password:str, pass_to_check:str)->bool:
    return my_context.verify(pass_to_check,hashed_password)

def create_jwt_token(data:UserLoginSignUp):
    expire_utc_unix=int((datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp())

    payload={"sub":data.user_id, "exp":expire_utc_unix}
    encoded_jwt=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def decode_jwt(token:str):
    try:
        payload=jwt.decode(token,key=SECRET_KEY,algorithms=ALGORITHM)
        return payload.get("sub")
    except:
        return None