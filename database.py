# from fastapi import HTTPException, status
# from sqlalchemy import create_engine
# from sqlalchemy.exc import OperationalError, ProgrammingError
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# from config import settings

# engine = create_engine(settings.database_url)
# Session_Local = sessionmaker(bind=engine, autocommit=False, autoflush=False)
# Base = declarative_base()


# def get_db():
#     db = Session_Local()
#     try:
#         yield db
#     except OperationalError as e:
#         print(e)
#         raise HTTPException(
#             status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Contect Admin"
#         )
#     except ProgrammingError as e:
#         print(e)
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Contect Admin"
#         )
#     finally:
#         db.close()
