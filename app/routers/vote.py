from fastapi import Depends,status,HTTPException,APIRouter
from sqlalchemy.orm import Session
from .. import schemas,database,models,oauth2
router=APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,db:Session=Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user)):
    post=db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id:{vote.post_id} does not exit")
    vote_query=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id,models.Vote.user_id==current_user.id)
    found_vote=vote_query.first()
    if (vote.dir==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
            detail=f"User {current_user.id} has already voted for voted on post {vote.post_id}")
        new_vote=models.Vote(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"Successfully added Vote"}
    else:
        if not found_vote:                     #Vote does not exist means current user not voted for thsis post
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"Successfully deleted vote"}
#for join                               tablefirst.first_second_fk= tablesecond.pk
#select posts.id from posts left join users on posts.owner_id=users.id;
#we posts.id because of id present in both table(posts and users)
#select user.id,user.emailid, count(owner_id) as user_post_count from posts right join users on posts.owner_id=users.id gorup by user.id
#now i want after clicking like i want to see user deatails and count of like on that post
