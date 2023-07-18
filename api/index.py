from fastapi import FastAPI, HTTPException, Path, Query, middleware
import uvicorn
from pydantic import BaseModel
import threading
from uuid import uuid4
import sqlite3

db = ''

app = FastAPI(
    title="Nexthon",
    desciption="Boilerplate to build a FastAPI + NextJS + React",
    version="1.0.0",
)


class User(BaseModel):
    username: str
    password: str
    role: str
    id: int


users = {
    0: User(username="admin", password="admin", role="admin", id=0),
    1: User(username="user", password="user", role="user", id=1),
    2: User(username="user2", password="user2", role="supporter", id=2),
    3: User(username="user3", password="user3", role="supervisor", id=3),
}


@app.get('/api/')
async def read_all_users() -> dict:
    return {"body": users}


@app.get('/api/{id}')
async def read_user(id: int, q: str = None):
    if id not in users:
        raise HTTPException(
            status_code=404, detail=f"User {user.id=} not found")
    return users[id]


@app.post('/api/?q={user}}')
async def add_user(user: User):
    if user.id in users:
        raise HTTPException(
            status_code=400, detail=f"User {user.id=} already exists")
    users.update(user)
    return {"added": user}


@app.put('/api/{id}', responses={404: {"Description": "user not found"}, 400: {"Description": "user already exists"}})
async def update_user(id: int, user: User):
    if id not in users:
        raise HTTPException(
            status_code=404, detail=f"User {user.id=} not found")
    users[id] = user
    return {"updated": user}


@app.delete('/api/{id}')
async def delete_user():
    if id not in users:
        raise HTTPException(
            status_code=404, detail=f"User {user.id=} not found")
    users.pop(id)
    return {"deleted": user}

if __name__ == '__main__':
    # comment to run in prod through the package.json file script
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
