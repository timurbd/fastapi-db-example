from fastapi.testclient import TestClient
import pytest

from main import app, Base, init_db

from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"  # SQLite database
engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False})

client = TestClient(app)


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    init_db()
    yield
    Base.metadata.drop_all(bind=engine)


def test_read_users(test_db):
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == [{'name': 'Arjen', 'age': 34, 'id': 1}]


def test_create_user(test_db):
    response = client.post("/users/", json={'name': 'Arjen',
                                            'age': 34})
    print(response.json())
    assert response.status_code == 201
