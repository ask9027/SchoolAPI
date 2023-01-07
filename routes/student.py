from fastapi import APIRouter, Depends, HTTPException, status
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
            detail=f"Roll Number: {student.rollNumber} Already Exists",
        )
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return stdDB


@route.get("/student_by_uid/{uid}", response_model=schemas.GetStudent)
def get_student_by_id(
    uid: str,
    db: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):
    student = db.query(models.Student).filter(models.Student.uid == uid).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student Not Found",
        )
    return student
