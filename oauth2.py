from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

import database
import models
import schemas
from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_WEEKS = settings.access_token_expire_weeks


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(weeks=ACCESS_TOKEN_EXPIRE_WEEKS)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


def verify_access_token(token: str, db, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        uid = payload.get("user_uid")
        if uid is None:
            raise credentials_exception

        black_list_token = (
            db.query(models.TokenBlackList)
            .filter(models.TokenBlackList.token == token)
            .first()
        )

        if black_list_token:
            raise credentials_exception
        token_data = schemas.TokenData(uid=uid)

    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate cresentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token, db, credentials_exception)
    current_user = (
        db.query(models.User).filter(models.User.uid == token_data.uid).first()
    )
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found"
        )
    return current_user


def get_user_token(token: str = Depends(oauth2_scheme)):
    return token
