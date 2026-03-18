import json
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.database.connection import result
from app.repositories import moderator_repository
from app.schemas.moderator_schema import AcknowledgeEventRequest, ClaimEventRequest, LoginRequest, ExpireEventRequest, \
    EventMetricsRequest
from app.schemas.response_builder import success_response, error_response
from app.utils.jwt_handler import create_access_token


def login_moderator(db: Session, request:LoginRequest):

    moderator = moderator_repository.get_moderator(db, request)
    if not moderator:
        return error_response("Moderator not found")

    token = create_access_token({
        "moderator_id": moderator.moderator_id,
        "moderator_name": moderator.moderator_name
    })

    return success_response(
        "Login successful",
        {
            "moderator_id": moderator.moderator_id,
            "moderator_name": moderator.moderator_name,
            "region_id": moderator.moderator_region_id,
            "access_token": token,
            "token_type": "Bearer"
        }
    )


def get_available_events(db: Session, region_id:int, pagination: dict):
    if not region_id:
        return error_response("Region ID missing")
    events , pagination_data = moderator_repository.get_events_for_region(db, region_id, pagination)
    if not events:
        return error_response("No Events not found")

    event_list = []

    for event in events:
        event_list.append({
            "event_id": event.event_id,
            "category_name": event.category_name,
            "event_title": event.event_title,
            "event_description": event.event_description,
            "claimed_status": event.claimed_status
        })

    return success_response("List of Events", event_list, pagination_data)


def claim_event(db: Session, request: ClaimEventRequest):
    result =  moderator_repository.claim_event(db, request)
    if result == "NOT_FOUND":
        return error_response("No such event exists")

    if result == "ALREADY_CLAIMED":
        return error_response("Event already claimed.")

    return success_response(
        "Event successfully claimed",
        {
            "event_id": result["event_id"],
            "expire_time": result["expire_time"],
            "event_title": result["event_title"],
            "event_description": result["event_description"]
        })


def acknowledge_event(db: Session,request: AcknowledgeEventRequest):
    result = moderator_repository.acknowledge_event(db, request)

    if result["status"] == "NOT_FOUND":
        return error_response("Assignment not found.")

    if result["status"] == "EXPIRED":
        return error_response("Event expired. Please claim it again.")

    return success_response(
        "Event acknowledged.",
        {
            "event_id": result["event_id"],
            "ack_time": result["ack_time"]
        }
    )

def expire_event(db: Session, request:ExpireEventRequest):
    return moderator_repository.expire_event(db, request.event_id, request.moderator_id)

def expire_stale_assignments(db: Session):

    now = datetime.now(timezone.utc)

    expired_assignments = moderator_repository.get_total_expired_events(db, now)

    expired_count = 0

    for event, assignment in expired_assignments:

        moderator_repository.expire_event(db, event.event_id, assignment.moderator_id)

        expired_count += 1

    return expired_count

def get_active_claim(db: Session, moderator_id: int):

    assignment = moderator_repository.get_active_assignment(db, moderator_id)

    if not assignment:
        return None

    now = datetime.now(timezone.utc)
    expire_time = assignment.expire_time.replace(tzinfo=timezone.utc)

    if expire_time <= now:
        return None

    event = assignment.event
    return success_response(
        "Active claimed event",
        {
            "event_id": event.event_id,
            "category_name": event.category.category_name,
            "event_title": event.event_title,
            "event_description": event.event_description,
            "expire_time": assignment.expire_time
        }
    )

def ack_pending_events(db: Session, moderator_id: int):
    results = moderator_repository.pending_events(db, moderator_id)

    if not results:
        return success_response("No Events", [])

    events = [
        {
            "event_id": r.event_id,
            "expire_time": r.expire_time,
            "event_title": r.event_title,
            "event_description": r.event_description
        }
        for r in results
    ]

    return success_response("Events Pending", events)

def event_metrics(db: Session, region_id:int, moderator_id:int):
    result = moderator_repository.get_event_metrics(db, region_id, moderator_id)
    return success_response("Events Metrics", result)
