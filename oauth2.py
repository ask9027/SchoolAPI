import pyrebase
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
firebase = pyrebase.initialize_app(settings.dict())

auth = firebase.auth()


def get_current_user(token: str = Depends(oauth2_scheme)):
    print(token)
    user = auth.get_account_info(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
