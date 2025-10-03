from fastapi import FastAPI
from sqlmodel import SQLModel, Field

app = FastAPI()

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    password: str
    email: str = None
    is_active: bool = True
    
user_db = [
    User(id=1, username="admin", password="admin123", email="admin@mail.com", is_active=True),
    User(id=2, username="user1", password="pass1", email="user1@mail.com", is_active=True),
    User(id=3, username="user2", password="pass2", email="user2@mail.com", is_active=True),
    User(id=4, username="test", password="test123", email="test@mail.com", is_active=True),
    User(id=5, username="guest", password="guest", email="guest@mail.com", is_active=False)
]


@app.post("/users")
def create_user(user: User):
    if any(u.username == user.username for u in user_db):
        return {"status": "error", "message": "Username ya existe"}
    user.id = len(user_db) + 1
    user_db.append(user)
    return user

@app.get("/users")
def list_users(page: int = 1, size: int = 10):
    start = (page - 1) * size
    end = start + size
    return user_db[start:end]                                         

@app.get("/users/{id}") 
def get_user(id: int):
    for user in user_db:
        if user.id == id:
            return   
    return {"status": "error", "message": "Usuario no encontrado"}

@app.put("/users/{id}")
def update_user(id: int, username: str = None, email: str = None, is_active: bool = None):
    for user in user_db:
        if user.id == id:
            if username:
                user.username = username
            if email:
                user.email = email
            if is_active is not None:
                user.is_active = is_active
            return user
    return {"status": "error", "message": "Usuario no encontrado"}

@app.delete("/users/{id}")
def delete_user(id: int):
    for user in user_db:
        if user.id == id:
            user_db.remove(user)
            return {"status": "ok", "message": "Usuario eliminado"}
    return {"status": "error", "message": "Usuario no encontrado"}

@app.post("/login")
def login(username: str, password: str):
    for user in user_db:
        if user.username == username and user.password == password:
            return {"status": "ok", "message": "Login correcto"}
    return {"status": "error", "message": "Usuario o contraseña incorrectos"}