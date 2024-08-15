"""File that handles the database configuration"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

if os.getenv('DATABASE_URL') != None:
    SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL')
else:
    SQLALCHEMY_DATABASE_URL = 'postgresql://devuser:changeme@db:5432/devdb'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """ Function that returns a database session """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_db():
    """ Function that returns a database session for testing """

    SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
    test_engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()