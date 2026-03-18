from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
import time
import os
from dotenv import load_dotenv

# PostgreSQL connection details
load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

DEFAULT_DB_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres"

engine_default = create_engine(DEFAULT_DB_URL)

# Retry until postgres is ready
retries = 10
delay = 3

for attempt in range(retries):
    try:
        with engine_default.connect() as conn:
            conn.execute(text("COMMIT"))

            result = conn.execute(
                text(f"SELECT 1 FROM pg_database WHERE datname='{DB_DATABASE}'")
            )

            exists = result.scalar()

            if not exists:
                conn.execute(text(f"CREATE DATABASE {DB_DATABASE}"))
                print(f"Database {DB_DATABASE} created")
            else:
                print(f"Database {DB_DATABASE} already exists")

        break

    except OperationalError:
        print(f"Database not ready... retrying ({attempt+1}/{retries})")
        time.sleep(delay)

# Now connect to actual database
DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"

print("DATABASE_URL: ", DATABASE_URL)


engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=1800
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def connectDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()