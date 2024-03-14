#!/usr/bin/env python3
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

# Pydantic model for a user
class User(BaseModel):
    name: str
    age: int

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname="users", 
    user="postgres", 
    password="password", 
    host="localhost",
    cursor_factory=RealDictCursor # Allows accessing the results as a dictionary
)
cursor = conn.cursor()

# Create the users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
)
''')
conn.commit()    

@app.post("/users/", response_model=User, status_code=201)
def create_user(user: User):
    cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (user.name, user.age))
    conn.commit()    
    return user

@app.get("/users/", response_model=List[User])
def get_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    result = []
    for u in users:
        result.append(User(**u))
    return result
