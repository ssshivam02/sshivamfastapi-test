from urllib.request import Request
from fastapi import APIRouter,status,Depends,Request
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from tests.test_simple import test_add

router=APIRouter(tags=['Miscellaneous'])

@router.get("/",status_code=status.HTTP_200_OK)
async def root():
    return {"message":"Hello World! successfully deployed on heroku using github-action!!"}

#------------------------------------------------------------------------------------------------#    
@router.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    post=db.query(models.Post).all()
    #print(post)
    #this return sql query SELECT posts.id AS posts_id, posts.title AS posts_title, posts.content AS posts_content, posts.published 
#AS posts_published, posts.created_at AS posts_created_at
#FROM posts
    return {"Connection":"Success"}
#----------------------------------------------------------------------------------------------------#
