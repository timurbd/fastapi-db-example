#!/usr/bin/env python3
from fastapi import FastAPI, Depends
from pydantic import BaseModel, ConfigDict
from typing import List
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy.orm
from contextlib import asynccontextmanager
import os

# export DATABASE_URL="postgresql://postgres:password@localhost/users" <== 12 factor app
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./users.db")  

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = sqlalchemy.orm.declarative_base()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

def init_db():
    # Create all tables in the database
    Base.metadata.create_all(bind=engine)
    seed_db()

def seed_db():
    print("Seeding DB")
    db = SessionLocal()

    # Check if the tables are empty and seed data if they are
    if db.query(User).count() == 0:
        users = [
            User(name='Arjen', age=34),
        ]
        db.add_all(users)
        db.commit()

    db.close()

    
app = FastAPI(lifespan=lifespan)

# Pydantic model for a user
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)    

# Create the database tables
Base.metadata.create_all(bind=engine)

# Pydantic model for creating a user (without ID)
class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    age: int

# Pydantic model for reading a user (includes ID)
class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    age: int

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.post("/users/", response_model=UserRead, status_code=201)
def create_user(user: UserCreate, db=Depends(get_db)):
    db_user = User(name=user.name, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[UserRead])
def get_users(db=Depends(get_db)):
    return db.query(User).all()
