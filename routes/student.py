from fastapi import APIRouter, Depends, HTTPException, status,Response
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

import models
import oauth2
import schemas
from database import get_db

route = APIRouter(prefix="/user", tags=["Current User"])


@route.get("/students", response_model=list[schemas.GetStudent])
def get_students(
    db: Session = Depends(get_db), cureent_user=Depends(oauth2.get_current_user)
):
    students = db.query(models.Student).order_by(models.Student.rollNumber).all()
    return students


@route.post(
    "/add_student",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.GetStudent,
)
def add_student(
    student: schemas.Student,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    s = student.dict()
    stdDB = models.Student(**s)
    try:
        db.add(stdDB)
        db.commit()
        db.refresh(stdDB)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Roll number {student.rollNumber} already exists",
        )
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return stdDB


@route.put("/update_student", response_model=schemas.GetStudent)
def update_student(
    student: schemas.GetStudent,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    db_st = db.query(models.Student).filter(models.Student.uid == student.uid)
    if not db_st.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student Not Found",
        )

    try:
        db_st.update(student.dict(), synchronize_session=False)
        db.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Roll number {student.rollNumber} already exists",
        )
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return db_st.first()

@route.delete("/delete_student/{uid}")
def delete_student(uid:str,db:Session=Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    db_st=db.query(models.Student).filter(models.Student.uid == uid)
    if not db_st.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Student not found")
    try:
        db_st.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(status_code=status.HTTP_204_NO_CONTENT)