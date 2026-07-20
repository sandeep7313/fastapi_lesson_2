import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Check if DATABASE_URL is missing or contains placeholder values like "@host"
if not DATABASE_URL or "@host" in DATABASE_URL or "user:password" in DATABASE_URL:
    print("WARNING: Valid DATABASE_URL not found in .env. Falling back to local SQLite database (temp.db).")
    DATABASE_URL = "sqlite:///./temp.db"

if DATABASE_URL.startswith("postgres://"):
    # SQLAlchemy requires "postgresql://" instead of "postgres://"
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Configure engine arguments
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()

# Dependency to get database session in path operations
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

