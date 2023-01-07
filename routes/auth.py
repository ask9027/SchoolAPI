from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.exc import OperationalError, IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

import models
import oauth2
import schemas
import utils
from database import get_db
from oauth2 import create_access_token

route = APIRouter(prefix="/auth", tags=["Authentication"])


@route.post("/login")
def login(
    user_credential: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    try:
        user = (
            db.query(models.User)
            .filter(models.User.email == user_credential.username)
            .first()
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="!Invalid credentials"
            )
        if not utils.verify_pass(user_credential.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="!Invalid credentials"
            )
        access_token = create_access_token(data={"user_uid": user.uid})
        token = schemas.Token(access_token=access_token, token_type="Bearer")
    except OperationalError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return token


@route.get("/get_current_user", response_model=schemas.GetUser)
def get_current_user(current_user=Depends(oauth2.get_current_user)):
    return current_user


@route.post("/logout")
def logout(
    token: str = Depends(oauth2.get_user_token),
    db: Session = Depends(get_db),
    current_user: schemas.UserLogin = Depends(oauth2.get_current_user),
):
    black_token = {"token": token, "email": current_user.email}
    try:
        bTotken = models.TokenBlackList(**black_token)
        db.add(bTotken)
        db.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Already Loged Out"
        )
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return {"message": "Logout successfully"}
