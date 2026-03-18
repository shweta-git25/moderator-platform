from app.database.connection import engine, Base, SessionLocal
from app.database.models import Moderator
from app.database.SeedData import seed_master_data


def init_db():

    # Create tables
    Base.metadata.create_all(bind=engine)


    db = SessionLocal()

    # Prevent duplicate seeding
    if not db.query(Moderator).first():
        print("Seeding Master Data into tables...")
        seed_master_data()

    db.close()