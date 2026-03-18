from pydantic import BaseModel, Field
from typing import Any, Optional, Dict

class LoginRequest(BaseModel):
    moderator_name: str = Field(..., min_length=3)
    moderator_region_id: int = Field(..., gt=0)

class EventRequest(BaseModel):
    region_id: int = Field(..., gt=0)

class ClaimEventRequest(BaseModel):
    event_id: int= Field(..., gt=0)
    region_id: int = Field(..., gt=0)
    moderator_id: int = Field(..., gt=0)

class AcknowledgeEventRequest(BaseModel):
    event_id: int = Field(..., gt=0)
    moderator_id: int = Field(..., gt=0)

class ExpireEventRequest(BaseModel):
    event_id: int = Field(..., gt=0)
    moderator_id: int = Field(..., gt=0)

class EventResponse(BaseModel):
    event_id: int
    category_name: str
    event_title: str
    event_description: str
    claimed_status: int

class Pagination(BaseModel):
    page: int
    limit: int
    total_records: int
    total_pages: int


class BaseResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    pagination: Optional[Pagination] = None

    class Config:
        extra = "ignore"

class EventMetricsRequest(BaseModel):
    region_id: int = Field(..., gt=0)
    moderator_id: int = Field(..., gt=0)