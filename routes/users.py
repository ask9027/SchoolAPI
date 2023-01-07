from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

import models, schemas, utils, oauth2
from database import get_db

route = APIRouter(prefix="/users", tags=["Users"])


# @route.get("", response_model=list[schemas.GetUser])
# def get_users(
#     db: Session = Depends(get_db), cureent_user=Depends(oauth2.get_current_user)
# ):
#     usersList = db.query(models.User).order_by(models.User._id).all()
#     return usersList


@route.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.GetUser)
def add_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    hashed_pass = utils.hashPass(user.password)
    user.password = hashed_pass
    u = user.dict()
    usrDB = models.User(**u)
    try:
        db.add(usrDB)
        db.commit()
        db.refresh(usrDB)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User Already Exists"
        )
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return usrDB


# @route.get("/{user_id}", response_model=schemas.GetUser)
# def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User._id == user_id).first()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"User id `{user_id}` Not Found",
#         )
#     return user


# @route.put("/{user_id}", response_model=schemas.GetUser)
# def update_user_by_id(user_id: int, user: schemas.User, db: Session = Depends(get_db)):
#     oldUser = db.query(models.User).filter(models.User._id == user_id)

#     if not oldUser.first():
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"User Id `{user_id}` Not Found",
#         )
#     user.name = user.name.title()
#     nUser = user.dict()
#     try:
#         oldUser.update(nUser, synchronize_session=False)
#         db.commit()
#     except IntegrityError:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail=f"User {user.name} already exist",
#         )
#     except SQLAlchemyError:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     return oldUser.first()


# @route.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User._id == user_id).first()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"User Id `{user_id}` Not Found",
#         )
#     db.delete(user)
#     db.commit()
#     return
