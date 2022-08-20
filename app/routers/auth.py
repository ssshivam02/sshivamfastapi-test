from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status,HTTPException,Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas,models,utils,oauth2
router=APIRouter(tags=['Authorization'])

#OAuth2PasswordRequestForm stores useremail into field called username 
@router.post('/login',response_model=schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Invalid Credentials")
    if not utils.verify(user_credentials.password,user.password):        
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Invalid Credentials")
    
    #create a token                        #in data we add many other key
    access_token= oauth2.create_access_token(data={"user_id":user.id})
    return {"access_token":access_token,"token_type":"bearer"}

