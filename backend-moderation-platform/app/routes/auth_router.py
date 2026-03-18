from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import connectDB
from app.services import moderator_service
from app.schemas.moderator_schema import LoginRequest

router = APIRouter(prefix="/moderator", tags=["Authentication"])

# 1 Login Moderator
@router.post("/login")
def login_moderator(request: LoginRequest,db: Session = Depends(connectDB)):
    return moderator_service.login_moderator(db, request)