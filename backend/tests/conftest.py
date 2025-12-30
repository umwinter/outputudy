import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.infrastructure.database import Base, get_db

# Import models to ensure they are registered with Base.metadata
from app.infrastructure.orm_models import UserORM  # noqa: F401
from app.main import app


def get_worker_id():
    # gw0, gw1, etc. if running with xdist
    return os.environ.get("PYTEST_XDIST_WORKER", "master")


@pytest.fixture(scope="session")
def engine():
    worker_id = get_worker_id()
    db_path = f"test_{worker_id}.db"
    database_url = f"sqlite:///./{db_path}"

    engine = create_engine(database_url, connect_args={"check_same_thread": False})

    # Ensure tables are created for the isolated test database
    Base.metadata.create_all(bind=engine)
    yield engine

    # Cleanup database file after session
    try:
        if os.path.exists(db_path):
            os.remove(db_path)
    except Exception:
        pass


@pytest.fixture
def db_session(engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    # Cleanup overrides after each test
    app.dependency_overrides.clear()
