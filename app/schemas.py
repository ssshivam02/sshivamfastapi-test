from pydantic import BaseModel,EmailStr, conint, constr
from datetime import datetime
from typing import Optional
'''
#BaseModel for creating schema
class Post(BaseModel):
    #string type for title and content
    #this also checking type and proper input
    title: str
    content: str
    published: bool=True #default value
    #optional
    #rating: Optional[int]= None
'''
'''
class CreatePost(BaseModel):
    title: str
    content: str
    published: bool=True

class UpdatePost(BaseModel):
    title: str
    content: str
    published: bool=True
'''
class PageFastApi(BaseModel):
    created_at: datetime
    content:str
    id:int
    owner_id:int
    published: bool=True
    title: str
    
    class Config:
        orm_mode=True

class UserCreate(BaseModel):
    email:EmailStr
    password:str #we change it to hash for password
    phone_number:Optional[constr(min_length=10,max_length=10)]

    
class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    phone_number:Optional[constr(min_length=10,max_length=10)]

    class Config:
        orm_mode=True
class UserLogin(BaseModel):
    email:EmailStr
    password:str
#no need of creating my class and update or create can be consider in same class
class PostBase(BaseModel):
    title:str
    content:str
    published: bool=True

#now we can extend this class
class PostCreate(PostBase):
    pass


#response what we giving to user in response
#by add this schema in main we not get id and created_At
class Post(PostBase):
    id:int #if we want id must be show in response
    created_at:datetime
    owner_id:int
    owner:UserOut
    #this is because for giving dict type to pdantic model
    #this convert sqlalchemy into dict type
    class Config:
        orm_mode=True
class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        orm_mode=True

class Token(BaseModel):
    access_token:str
    token_type:str
class TokenData(BaseModel):
    id:Optional[str]= None

class Vote(BaseModel):
    post_id: str
    dir:conint(le=1)
#le means less than or equal to 1
#dir = is a vote direction for a post, dir= 1 means we want to add a like vote, dir= 0 means we want to delete a like vote 
