#!/usr/bin/env python3
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import sqlite3

app = FastAPI()

# Pydantic model for a user
class User(BaseModel):
    name: str
    age: int

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('example.db', check_same_thread=False)
cursor = conn.cursor()

# Create the users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
)
''')
conn.commit()    

@app.post("/users/", response_model=User, status_code=201)
def create_user(user: User):
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (user.name, user.age))
    conn.commit()
    return user

@app.get("/users/", response_model=List[User])
def get_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    result = []
    for row, name, age in users:
        result.append(User(name=name, age=age))
    return result
