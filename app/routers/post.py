from fastapi import Depends, Request,Response,status,HTTPException,APIRouter
from .. import models,schemas,oauth2
from fastapi_pagination import Page, add_pagination, paginate
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from fastapi_pagination import Page, add_pagination, paginate,Params

router = APIRouter(
    prefix="/posts",tags=['POST']
)
@router.get('/paginationfastapi',response_model=Page[schemas.PageFastApi])
async def read_posts(db: Session = Depends(get_db),params: Params = Depends()):
    data=db.query(models.Post).all()
    return paginate(data, params)
add_pagination(router)

# Query parameters
@router.get("/page")
def read_posts(page_num: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    start = (page_num - 1) * page_size
    end = start + page_size
    data=db.query(models.Post).all()
    response = {
        "data": data[start:end],
        "total": len(data),
        "count": page_size,
        "pagination": {}
    }

    if end >= len(data):
        response["pagination"]["next"] = None

        if page_num > 1:
            response["pagination"]["previous"] = f"/page?page_num={page_num-1}&page_size={page_size}"
        else:
            response["pagination"]["previous"] = None
    else:
        if page_num > 1:
            response["pagination"]["previous"] = f"/page?page_num={page_num-1}&page_size={page_size}"
        else:
            response["pagination"]["previous"] = None

        response["pagination"]["next"] = f"/page?page_num={page_num+1}&page_size={page_size}"

    return response

@router.get("/pagination", status_code=status.HTTP_200_OK)
def get_page(page_num:Optional[int]=1,page_size:Optional[int]=5,db: Session = Depends(get_db)):
    post=db.query(models.Post).all()
    start=(page_num-1)*page_size
    end=start+page_size
    return post[start:end]
#by using orm
#in get we get list in return so we need List[]
#@router.get("/",response_model=List[schemas.Post])        #int is not imp we can add anything here #limit 10 is default
@router.get("/", response_model=List[schemas.PostOut])        #int is not imp we can add anything here #limit 10 is default
def get_posts(db: Session = Depends(get_db),current_user:int= Depends(oauth2.get_current_user),
limit:Optional[int]=10,skip:Optional[int]=0,search:Optional[str]= ""):
    #{{URL}}posts?limit=5&skip=0&search=this%my
    #this will make private as per owner_id
    #post=db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
    #for accessing limit in url we need to add posts?limit=3 or for default we use posts? only
    #for adding skip in our url we need to add posts?limit=3&skip=0
    #for seraching url posts?limit=3&skip=3&search=king
    #for seraching url posts?limit=3&skip=3&search=king%is%best % for spaces between word
    post=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #we func for aggregation function and .label is using for setting column name
    results=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
    models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # In sqlalchemy by default the join is doing left inner join but we want (null) and we want left outer join
    return results
    #we can remove "data"
    #return post.


#by sql
'''
@app.get("/posts",status_code=status.HTTP_202_ACCEPTED)
def get_posts():
    cursor.execute("""select * from posts""")
    my_post= cursor.fetchall()
    print(my_post)
    return {"data": my_post}
'''

#by using orm #use of response_model is imp
@router.post("/create",response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
async def post_create(post:schemas.PostCreate,req:Request,db: Session = Depends(get_db),current_user:int= Depends(oauth2.get_current_user)):
    #print(post.dict())
    ans=await req.json()
    #if we have many column then we can use **post.dict() this will unpack automatically
    #new_post=models.Post(title=post.title,content= post.content, published= post.published)
    #add then commiting
    #print(current_user.id)
    new_post=models.Post(**post.dict(),owner_id=current_user.id,)
    db.add(new_post)
    db.commit()
    # refresh as like returning *
    db.refresh(new_post)
    return new_post

#bysql
'''
@app.post("/",status_code=status.HTTP_201_CREATED)
def post_create(post:schemas.Post):
    print(post)                                     #%s we using to protecting our code from sql injection %s as like variable
    cursor.execute("""insert into posts (title,content,published) values (%s,%s,%s) returning * """,(post.title,post.content,post.published))
    # post_dict=post.dict()
    #new_post currently a pydantic model if we want to change this dict
    #print(post.dict())
    conn.commit()
    new_post=cursor.fetchone()
    return {"new post": new_post}
'''
'''
def find_post(id:int):
    for p in my_posts:
        if p["id"]==int(id):
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id']== id:
            return i
'''
#validation also possible by add int and str in argument in func
'''
@app.get("/{id}")
def get_post_id(id:int,response: Response):    # :int is checking type of id
    post=find_post(id)
    if not post:
        response.status_code=status.HTTP_404_NOT_FOUND 
        return {'message':f"post with  id: {id} was not found"}
    return {"post_details": post}
'''
#by using orm
@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,db: Session = Depends(get_db),current_user:int= Depends(oauth2.get_current_user)):
    #post=db.query(models.Post).filter(models.Post.id==id).first()
    post=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
    models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()

    #print(post) this will work after removing .first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with  id: {id} was not found")
    #by applying this two line our get method become private
    #if post.owner_id!=current_user.id:
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested action")

    return post


#better way of doing not found id by using httpexception
#by sql

'''
@app.get("/{id}")
def get_post(id:int):
    cursor.execute("""select *from posts where id = %s""",(str(id)))
    post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with  id: {id} was not found")
    return {"post_details": post}
'''
#by using orm
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user:int= Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with  id: {id} was not found")
    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT )


#by using sql
#delete
'''
@app.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    # find the index in the array that has required id
    #my_posts.pop(index)
    cursor.execute("""delete from posts where id =%s returning * """,(str(id)))
    post=cursor.fetchone()
    conn.commit()
    #index= find_index_post(id)
    if post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with  id: {id} was not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT )
'''
#by using orm

@router.put("/{id}")
def update_post(id: int,updated_post: schemas.PostCreate,db: Session = Depends(get_db),current_user:int= Depends(oauth2.get_current_user)):
    #index= find_index_post(id)
    #print(type(current_user))
    post_query= db.query(models.Post).filter(models.Post.id==id)
    post= post_query.first()
    if post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with  id: {id} was not found")
    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested action")
    #we can do updatation in one like also
    #db.query(models.Post).filter(models.Post.id==id).update(post.dict(),syncsynchronize_session=False)
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()

#by using sql
#update
'''
@app.put("/{id}")
def update_post(id: int,post: schemas.Post):
    #index= find_index_post(id)
    cursor.execute(""" update posts set title =%s, content=%s,published =%s where id=%s returning * """,
    (post.title,post.content,post.published,str(id)))
    post= cursor.fetchone()
    conn.commit()
    if post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with  id: {id} was not found")
    return {'message':post}
'''
