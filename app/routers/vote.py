from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils, oauth2

router = APIRouter(
    tags=["Votes"],
    prefix="/votes"
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(votes: schemas.Vote, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    post_exist_query = db.query(models.Post).filter(models.Post.id == votes.post_id).first()
    if not post_exist_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The Post With Id: {votes.post_id} Does Not Exist")
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == votes.post_id, models.Vote.user_id == current_user.id)

    found_vote = vote_query.first()
    if (votes.direction):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"{current_user.username} Can't Vote This Post Twice.")
        new_vote = models.Vote(post_id = votes.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully Added The Vote."}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"{current_user.username} Has Not Voted This Post Yet, Can't Delete Vote")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully Deleted The Vote."}