# Moderation Platform
A moderation platform that enables region-based event handling with real-time claiming, acknowledgment, and expiry control using FastAPI and PostgreSQL.

## System Overview Flow

Event Generated  
    ↓  
Stored in Database  
    ↓  
Visible to Region-Specific Moderators  
    ↓  
Moderator Claims Event  
    ↓  
Event Locked (15 min expiry starts)  
    ↓  
[Within 15 min] → Acknowledged → Completed ✅

## Run Project

1. Install Docker
2. Clone repository:  
3. Run using command:
   - docker-compose down -v  ----------- (Optional to remove existing container)
   - docker-compose up --build

Frontend
http://localhost:3000

Backend
http://localhost:8000/docs

You can use the hardcoded user with below details to login.
- User Id: user000
- Region Id: 1 (ASIA)



## Postman Collection:

Please create the below environment variables in the Postman.
- moderator_api_url = http://127.0.0.1:8000/moderator
- token

To run the docker - Postegres SQL Editor:

Command: docker exec -it moderator_postgres psql -U postgres -d moderator_db

To exit Query Editor: q

## Implemented Requirements:
- Moderator Login (Hardcoded User: user000 and Region: ASIA)
- View Available Events
- Claim an Event 
- Acknowledge an Event
- Automatic Expiry/Reassignment
- A scheduled job of Continuous Ingestion of Events with Assumption
- A scheduled job of Background worker for expiring stale assignments
- Exposing useful metrics
- Writing basic unit test cases in Postman

## Documentation: 
[📘 The Moderator Platform PDF](./The_Moderator_Platform.pdf)
