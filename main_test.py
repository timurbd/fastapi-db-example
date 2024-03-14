from fastapi import FastAPI
from fastapi.testclient import TestClient
import logging 
import pytest

from main import app

client = TestClient(app)

def test_read_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == []

def test_create_user():
    response = client.post("/users/", json={'name': 'Arjen',
                                            'age': 34})
    print(response.json())
    assert response.status_code == 201

    
