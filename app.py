from fastapi import FastAPI
from pydantic import BaseModel

from study_agent import generate_study_plan


# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="Study Planner Agent",
    description="AI-powered study planning assistant",
    version="1.0"
)


# --------------------------------------------------
# Request model
# --------------------------------------------------

class StudyRequest(BaseModel):
    request: str


# --------------------------------------------------
# Health check
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "status": "online",
        "message": "Study Planner Agent API is running"
    }


# --------------------------------------------------
# Study planning endpoint
# --------------------------------------------------

@app.post("/plan")
def create_plan(data: StudyRequest):

    result = generate_study_plan(data.request)

    return {
        "plan": result
    }