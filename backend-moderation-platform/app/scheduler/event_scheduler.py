import time
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.repositories import moderator_repository
from app.services import event_generator_service, moderator_service


scheduler = BackgroundScheduler()


def calculate_interval(unclaimed_count):

    interval = 15 + (unclaimed_count // 1000) * 15

    if interval > 1500:   # safety cap (100k events)
        interval = 1500

    return interval


# EVENT INGESTION SCHEDULER
def ingest_events():

    db: Session = SessionLocal()

    try:

        # count unclaimed events
        unclaimed = moderator_repository.get_total_available_events_count(db)

        # calculate dynamic interval
        interval = calculate_interval(unclaimed)

        print(f"Unclaimed events: {unclaimed}")
        print(f"Next batch interval running by Event Ingestion Scheduler: {interval} sec")

        # insert batch
        event_generator_service.event_generator_data(batch_size=20)

        # reschedule next run dynamically
        scheduler.reschedule_job(
            "event_ingestion_job",
            trigger="interval",
            seconds=interval
        )

    finally:
        db.close()


# BACKGROUND EXPIRY WORKER

def expire_stale_assignments():

    db: Session = SessionLocal()
    try:
        expired_count = moderator_service.expire_stale_assignments(db)

        if expired_count > 0:
            print(f"Expired Assignments cleaned up by Background Worker: {expired_count}")

    finally:
        db.close()


def start_scheduler():

    scheduler.add_job(
        ingest_events,
        "interval",
        seconds=15,
        id="event_ingestion_job",
        replace_existing=True
    )

    scheduler.add_job(
        expire_stale_assignments,
        "interval",
        seconds=30,
        id="expire_assignment_job",
        replace_existing=True
    )

    scheduler.start()

    print("Event Ingestion Scheduler and Assignment Expiry Worker started.")