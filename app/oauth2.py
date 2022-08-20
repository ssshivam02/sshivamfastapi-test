import uuid
from fastapi import Depends, HTTPException,status
from jose import JWTError,jwt
from datetime import datetime,timedelta
from .config import setting
from sqlalchemy.orm import Session

from app import models
from . import schemas,database
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')
def generate_uuid():
    return str(uuid.uuid4())

#three pieces of info for token creatation
#SECRET_KEY
#ALGORITHM
#EXPRESSION_TIME=

SECRET_KEY= setting.secret_key #generate_uuid()
ALGORITHM=setting.algorithm #"HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=setting.access_token_expire_minutes#60

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:str=payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data= schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data
    #token_data is user id only

def get_current_user(token:str=Depends(oauth2_scheme),db: Session=Depends(database.get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not valiadate credentitals",headers={"WWW-Authenticate":"Bearer"})
    token= verify_access_token(token,credentials_exception)
    user=db.query(models.User).filter(models.User.id==token.id).first()
    return user