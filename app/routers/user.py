from fastapi import Depends,status,HTTPException,APIRouter
from .. import models,schemas,utils
from sqlalchemy.orm import Session
from typing import List
from ..database import engine,get_db

router = APIRouter(
    prefix="/users",
    tags=['USER']
)

@router.post("/create", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db: Session = Depends(get_db)):
    #hash the password from user.password
    hassed_password=utils.hash(user.password)
    user.password=hassed_password
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 
    return new_user

@router.get('/{id}', response_model=schemas.UserOut)
def get_user_id(id: int, db: Session = Depends(get_db)):
    if user := db.query(models.User).filter(models.User.id == id).first():
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} doesnot found")
@router.get("/",response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    # sourcery skip: inline-immediately-returned-variable
    user=db.query(models.User).all()
    #print(post)
    #this return sql query SELECT posts.id AS posts_id, posts.title AS posts_title, posts.content AS posts_content, posts.published 
#AS posts_published, posts.created_at AS posts_created_at
#FROM posts
    return user
