from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from app.database.models import Moderator, Event, EventCategory, Assignment
from app.schemas.moderator_schema import AcknowledgeEventRequest, ClaimEventRequest, LoginRequest, ExpireEventRequest
from app.utils.pagination import paginate_query
from sqlalchemy import text

def get_moderator(db: Session, request:LoginRequest):
    moderator = db.query(Moderator).filter(
        Moderator.moderator_name == request.moderator_name,
        Moderator.moderator_region_id == request.moderator_region_id
    ).first()
    return moderator


def get_events_for_region(db: Session, region_id: int, pagination: dict):
    query = (
        db.query(
            Event.event_id,
            EventCategory.category_name,
            Event.event_title,
            Event.event_description,
            Event.claimed_status
        )
        .join(EventCategory, Event.category_id == EventCategory.category_id)
        .filter(Event.region_id == region_id, Event.claimed_status == 0)
        .order_by(Event.event_id)
    )

    return paginate_query(query, pagination)

def claim_event(db: Session, request: ClaimEventRequest):

    try:
        event_exist = (
            db.query(Event)
            .filter(
                Event.event_id == request.event_id,
                Event.region_id == request.region_id
            ).first()
        )
        if not event_exist:
            return "NOT_FOUND"

        event = (
            db.query(Event)
            .filter(
                Event.event_id == request.event_id,
                Event.region_id == request.region_id,
                Event.claimed_status == 0
            )
            .with_for_update()
            .first()
        )

        # case 1: no such event
        if not event:
            return "ALREADY_CLAIMED"


        # case 2: available then update
        event.claimed_status = 1
        now = datetime.now(timezone.utc)
        expire_time = now + timedelta(minutes=15)
        assignment = Assignment(
            event_id=request.event_id,
            moderator_id=request.moderator_id,
            claimed_time=datetime.now(),
            expire_time=expire_time,
            ack_status=0
        )

        db.add(assignment)

        db.commit()

        return {
            "status": "SUCCESS",
            "event_id": request.event_id,
            "expire_time": expire_time,
            "event_title":event.event_title,
            "event_description":event.event_description
        }

    except Exception as e:
        db.rollback()
        raise e

def acknowledge_event(db: Session, request: AcknowledgeEventRequest):
    assignment = (
        db.query(Assignment)
        .filter(
            Assignment.event_id == request.event_id,
            Assignment.moderator_id == request.moderator_id
        )
        .with_for_update()
        .first()
    )

    # Assignment not found
    if not assignment:
        return {"status": "NOT_FOUND"}

    expire_time = assignment.expire_time.replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)

    if now > expire_time:

        event = (
            db.query(Event)
            .filter(Event.event_id == request.event_id)
            .with_for_update()
            .first()
        )

        if event:
            event.claimed_status = 0


        db.commit()

        return {"status": "EXPIRED"}

    # Valid acknowledgement
    assignment.ack_status = 1
    assignment.ack_time = now

    db.commit()
    return {
        "status": "SUCCESS",
        "event_id": assignment.event_id,
        "ack_time": assignment.ack_time
    }

def expire_event(db: Session, event_id: int, moderator_id: int):

    result = (
                db.query( Event, Assignment)
                .join(Assignment, Event.event_id == Assignment.event_id)
                .filter(
                    Event.event_id == event_id,
                    Assignment.moderator_id == moderator_id,
                    Assignment.ack_status==0,
                    Event.claimed_status == 1
                )
                .first()
            )

    if result:
        # Mark the event as not claimed so it can be claimed by other moderators
        event = result.Event
        event.claimed_status = 0

        db.commit()

        return {
                "message": "Event expired",
                "event_id": event_id
            }
    else:
        return {
                "message": "No active Event found",
                "event_id": event_id
            }

def get_total_available_events_count(db: Session):
    return db.query(Event).filter(Event.claimed_status == 0).count()

def get_total_expired_events(db: Session, now):
    result = (
        db.query(Event, Assignment)
        .join(Assignment, Event.event_id == Assignment.event_id)
        .filter(
            Assignment.ack_status == 0,
            Assignment.expire_time <= now,
            Event.claimed_status == 1
        )
        .all()
    )
    return result

def get_active_assignment(db: Session, moderator_id: int):
    return (
        db.query(Assignment)
        .filter(
            Assignment.moderator_id == moderator_id,
            Assignment.ack_status == 0
        )
        .order_by(Assignment.claimed_time.desc())
        .first()
    )

from datetime import datetime

def pending_events(db: Session, moderator_id: int):
    return (
        db.query(
            Event.event_id,
            Event.event_title,
            Event.event_description,
            Assignment.expire_time
        )
        .join(Assignment, Assignment.event_id == Event.event_id)
        .filter(
            Assignment.moderator_id == moderator_id,
            Assignment.ack_status == 0,
            Assignment.expire_time > datetime.utcnow()
        )
        .all()
    )

def get_event_metrics(db: Session, region_id: int, moderator_id: int):
    query = text("""
            SELECT
                COUNT(e.event_id) AS total_events,

                COUNT(*) FILTER (
                    WHERE e.claimed_status = 1
                    AND a.ack_status = 0
                    AND a.moderator_id = :moderator_id
                ) AS total_assigned,

                COUNT(*) FILTER (
                    WHERE a.ack_status = 1
                    AND a.moderator_id = :moderator_id
                ) AS expired_events

            FROM tb_events e
            LEFT JOIN tb_assignment a
            ON a.event_id = e.event_id

            WHERE e.region_id = :region_id
        """)

    result = db.execute(
        query,
        {
            "region_id": region_id,
            "moderator_id": moderator_id
        }
    ).fetchone()

    return dict(result._mapping) if result else {}
