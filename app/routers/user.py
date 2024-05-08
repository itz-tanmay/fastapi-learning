from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # ? Check if a user with the same username already exists in the database
    existing_username = db.query(models.User).filter(
        models.User.username == user.username).first()
    existing_email = db.query(models.User).filter(
        models.User.email == user.email).first()
    if existing_username:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="The User With This Username Already Exists.")
    if existing_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="The User With This E-mail Already Exists.")

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User With Id: {id} Does Not Exist")

    return user
