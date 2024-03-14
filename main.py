#!/usr/bin/env python3
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Pydantic model for a user
class User(BaseModel):
    name: str
    age: int

# In-memory datastore
users: List[User] = []

@app.post("/users/", response_model=User, status_code=201)
def create_user(user: User):
    users.append(user)
    return user

@app.get("/users/", response_model=List[User])
def get_users():
    return users
