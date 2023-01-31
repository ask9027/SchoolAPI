from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import oauth2

route = APIRouter(prefix="/auth", tags=["Authentication"])


@route.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = oauth2.auth.sign_in_with_email_and_password(
        form_data.username, form_data.password
    )
    access_token = user["idToken"]
    print(access_token)
    return {"access_token": access_token, "token_type": "bearer"}


@route.get("/logout")
def logout(token=Depends(oauth2.get_current_user)):
    return "logout"
