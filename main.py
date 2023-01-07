from fastapi import FastAPI

from routes import users, auth, student

app = FastAPI(debug=True, title="School API")

app.include_router(auth.route)
app.include_router(users.route)
app.include_router(student.route)


@app.get("/")
def home():
    return "Home Page"
