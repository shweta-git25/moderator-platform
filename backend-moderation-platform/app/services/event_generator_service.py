from app.database.connection  import SessionLocal
from app.database.models import Region, Moderator, EventCategory, Event
import random

def event_generator_data(batch_size=10):

    session = SessionLocal()

    regions = session.query(Region).all()
    categories = session.query(EventCategory).all()

    titles = {
        "Equipment Safety": [
            "Forklift Brake Failure",
            "Conveyor Belt Overload",
            "Damaged Pallet Jack",
            "Crane Sensor Malfunction"
        ],
        "Storage Safety": [
            "Unstable Pallet Stack",
            "Blocked Emergency Exit",
            "Overloaded Storage Rack",
            "Improper Hazard Storage"
        ],
        "Worker Safety": [
            "Worker Without Helmet",
            "Unsafe Ladder Usage",
            "Worker in Restricted Zone",
            "Lack of Safety Vest"
        ],
        "Management Safety": [
            "Missing Safety Inspection",
            "Expired Safety Certification",
            "Incomplete Incident Report",
            "Ignored Safety Protocol"
        ],
        "Transport Safety": [
            "Unsecured Cargo",
            "Truck Dock Misalignment",
            "Driver Fatigue Alert",
            "Improper Trailer Lock"
        ]
    }

    descriptions = {
        "Equipment Safety": [
            "Forklift brake system reported malfunction during warehouse operation.",
            "Automated conveyor belt exceeded recommended load capacity.",
            "Pallet jack wheel damaged while transporting goods.",
            "Warehouse crane safety sensor not responding properly."
        ],
        "Storage Safety": [
            "Pallets stacked above recommended height limit.",
            "Emergency exit obstructed by stored inventory boxes.",
            "Heavy inventory stored beyond rack capacity.",
            "Hazardous materials placed outside designated storage."
        ],
        "Worker Safety": [
            "Worker observed without helmet in active loading zone.",
            "Employee using ladder without proper stabilization.",
            "Worker entered forklift movement zone without authorization.",
            "Safety vest missing in high traffic warehouse area."
        ],
        "Management Safety": [
            "Scheduled safety inspection not recorded in system.",
            "Safety training certification expired for warehouse staff.",
            "Incident report missing key safety details.",
            "Warehouse safety checklist not completed by supervisor."
        ],
        "Transport Safety": [
            "Cargo inside truck not secured before transport.",
            "Delivery truck improperly aligned with dock station.",
            "Driver fatigue warning triggered during long haul.",
            "Trailer lock not properly engaged before departure."
        ]
    }

    events = []

    for i in range(batch_size):

        category = random.choice(categories)
        region = random.choice(regions)

        category_name = category.category_name

        title = random.choice(titles[category_name])
        description = random.choice(descriptions[category_name])

        event = Event(
            category_id=category.category_id,
            region_id=region.region_id,
            event_title=title,
            event_description=description
        )

        events.append(event)

    session.add_all(events)
    session.commit()
    session.close()

    print(f"Events generated successfully by Event Ingestion Scheduler: {batch_size}")