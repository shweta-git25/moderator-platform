from app.database.connection  import SessionLocal
from app.database.models import Region, Moderator, EventCategory
import random

def seed_master_data():
    session = SessionLocal()

    # -------------------------
    # Regions
    # -------------------------
    regions_data = [
        {"region_code": "ASI", "region_name": "Asia"},
        {"region_code": "AFR", "region_name": "Africa"},
        {"region_code": "AUS", "region_name": "Australia"},
        {"region_code": "EUR", "region_name": "Europe"},
        {"region_code": "NAM", "region_name": "North America"},
        {"region_code": "SAM", "region_name": "South America"}
    ]

    regions = []
    for data in regions_data:
        region = Region(**data)
        regions.append(region)

    session.add_all(regions)
    session.commit()

    # -------------------------
    # Categories
    # -------------------------
    categories_data = [
        {"category_code": "EQPM", "category_name": "Equipment Safety"},
        {"category_code": "STRG", "category_name": "Storage Safety"},
        {"category_code": "WORK", "category_name": "Worker Safety"},
        {"category_code": "MGMT", "category_name": "Management Safety"},
        {"category_code": "TRNS", "category_name": "Transport Safety"}
    ]

    categories = []
    for data in categories_data:
        category = EventCategory(**data)
        categories.append(category)

    session.add_all(categories)
    session.commit()

    # -------------------------
    # Moderators (20 users)
    # -------------------------
    moderators = []

    # Hardcoded moderator
    hardcoded_user = Moderator(
        moderator_name="user000",
        moderator_region_id=1
    )
    moderators.append(hardcoded_user)

    for i in range(20):
        moderator = Moderator(
            moderator_name=f"user{str(i+1).zfill(3)}",
            moderator_region_id=random.choice(regions).region_id
        )
        moderators.append(moderator)

    session.add_all(moderators)
    session.commit()

    session.close()

    print("Regions, Categories and Moderators seeded successfully!")
