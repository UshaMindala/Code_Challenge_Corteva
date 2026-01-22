# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Using a local file-based DB for simplicity and development
SQLALCHEMY_DATABASE_URL = "sqlite:///./weather.db"                                         # SQLite database URL

# Create the SQLAlchemy engine
# check_same_thread=False is required for SQLite when
# using the same connection across multiple threads (e.g., FastAPI)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


# Factory for creating new database sessions
# autocommit=False and autoflush=False give us explicit control
# over when transactions are committed and flushed
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)