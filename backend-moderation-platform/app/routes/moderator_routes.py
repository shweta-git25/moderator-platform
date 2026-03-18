from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from app.database.connection import connectDB
from app.schemas.response_builder import error_response, success_response
from app.services import moderator_service
from app.schemas.moderator_schema import AcknowledgeEventRequest, ClaimEventRequest, LoginRequest, EventResponse, \
    ExpireEventRequest, EventMetricsRequest
from app.utils.auth_dependency import get_current_user
from app.utils.pagination import get_pagination

router = APIRouter(prefix="/moderator", tags=["Moderator"], dependencies=[Depends(get_current_user)])


# 2 Get Available Events
@router.get("/events/{region_id}")
def get_available_events(region_id: int | None = None, db: Session = Depends(connectDB), pagination: dict = Depends(get_pagination)):
    return moderator_service.get_available_events(db, region_id, pagination)


# 3 Claim Events
@router.post("/claim")
def claim_event(request: ClaimEventRequest, db: Session = Depends(connectDB)):
    return moderator_service.claim_event(db, request)


# 4 Acknowledge Event
@router.post("/acknowledge")
def acknowledge_event(request: AcknowledgeEventRequest, db: Session = Depends(connectDB)):
    return moderator_service.acknowledge_event(db, request)

@router.post("/expire")
def expire_event(request:ExpireEventRequest, db: Session = Depends(connectDB)):
    return moderator_service.expire_event(db, request)

@router.get("/active-claim/{moderator_id}")
def active_claim(moderator_id: int, db: Session = Depends(connectDB)):
    return moderator_service.get_active_claim(db, moderator_id)

@router.get("/ack-pending-events/{moderator_id}")
def active_claim(moderator_id: int, db: Session = Depends(connectDB)):
    return moderator_service.ack_pending_events(db, moderator_id)

@router.get("/event-metrics")
def event_metrics(region_id: int,moderator_id: int,db: Session = Depends(connectDB)):
    return moderator_service.event_metrics(db, region_id, moderator_id)