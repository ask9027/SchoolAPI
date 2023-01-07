from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashPass(password: str):
    return pwd_context.hash(password)


def verify_pass(password: str, hashed_pass: str):
    return pwd_context.verify(password, hashed_pass)
