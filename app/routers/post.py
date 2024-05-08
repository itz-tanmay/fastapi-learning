from fastapi import HTTPException, status, Depends, APIRouter, Response
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, oauth2
from typing import List, Optional


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get('', response_model=List[schemas.PostResponseWithVotes])
# @ GET Method
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).order_by(models.Post.id).filter(models.Post.title.contains(
            search)).order_by(models.Post.id).limit(limit).offset(skip).all()
    return posts


@router.post('/create-post', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):  # @ POST Method
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # post = cursor.fetchone()
    # conn.commit()

    # REMEMBER we have to do like this => ourDatasetModel(unpacking ourSchemaModel Value)
    # print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.PostResponseWithVotes)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):  # @ GET(specific) Method

    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id,))
    # post = cursor.fetchone()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The Post With Id: {id} Does Not Exist")
    return post


@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):  # @ DELETE Method
    deleted_post_query = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The Post With Id: {id} Does Not Exist")

    if deleted_post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Unauthorized Action. Don't Have Permission TO Perform Requested Action.")

    deleted_post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/update/{id}', response_model=schemas.PostResponse)
# @ PUT[UPDATE] Method
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()
    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The Post With Id: {id} Does Not Exist"
        )
    if post_query.first().id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Unauthorized Action. Don't Have Permission TO Perform Requested Action.")
    post_query.update(post.model_dump(exclude_unset=True),
                      synchronize_session=False)
    db.commit()
    return post_query.first()
