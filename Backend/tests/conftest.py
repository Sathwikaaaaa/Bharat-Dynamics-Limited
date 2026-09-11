import os

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import Base
from app.database import models


load_dotenv()


DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

TEST_DB_NAME = os.getenv(
    "TEST_DB_NAME",
    "invoice_test_db"
)


if not DB_PASSWORD:
    raise RuntimeError(
        "DB_PASSWORD is not configured."
    )


TEST_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}"
)


@pytest.fixture
def test_db():

    test_engine = create_engine(
        TEST_DATABASE_URL,
        pool_pre_ping=True
    )

    Base.metadata.create_all(
        bind=test_engine
    )

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine
    )

    db = TestingSessionLocal()

    try:

        yield db

    finally:

        db.close()

        Base.metadata.drop_all(
            bind=test_engine
        )

        test_engine.dispose()