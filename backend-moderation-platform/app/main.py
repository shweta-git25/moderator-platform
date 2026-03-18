from fastapi import FastAPI, Request
from app.database.init_db import init_db
from app.routes import moderator_routes, auth_router
from app.scheduler import event_scheduler
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Ensure tables exist (optional)

init_db()

origins = [
    "http://localhost:3000",   # React app
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(moderator_routes.router)


@app.get("/")
def home():
    return {"message": "Moderation API running"}

@app.on_event("startup")
def start_background_jobs():
    event_scheduler.start_scheduler()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    messages = []

    for err in exc.errors():
        field = err["loc"][-1]
        error_type = err["type"]

        if error_type == "missing":
            messages.append(f"{field} is required")

        elif "int" in error_type:
            messages.append(f"{field} must be an integer")

        elif "string" in error_type:
            messages.append(f"{field} must be a string")

        else:
            messages.append(err["msg"])

    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": ", ".join(messages),
            "data": None,
        }
    )