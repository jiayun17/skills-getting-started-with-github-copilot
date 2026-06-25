"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Team drills, games, and basketball skills development",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["chris@mergington.edu", "maya@mergington.edu"]
    },
    "Soccer Club": {
        "description": "Soccer practice, fitness, and friendly matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["alex@mergington.edu", "riley@mergington.edu"]
    },
    "Drama Club": {
        "description": "Acting workshops, rehearsals, and performance preparation",
        "schedule": "Wednesdays, 5:00 PM - 6:30 PM",
        "max_participants": 16,
        "participants": ["lily@mergington.edu", "noah@mergington.edu"]
    },
    "Art Studio": {
        "description": "Creative art projects, painting, drawing, and sculpture",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["mia@mergington.edu", "ethan@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Prepare for science competitions and explore STEM challenges",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["oliver@mergington.edu", "ava@mergington.edu"]
    },
    "Math Challenge": {
        "description": "Problem-solving sessions and competition preparation",
        "schedule": "Mondays, 4:00 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["sophia@mergington.edu", "liam@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Normalize the email for consistent duplicate checking
    normalized_email = email.strip().lower()
    if not normalized_email:
        raise HTTPException(status_code=400, detail="Email is required")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    normalized_participants = [participant.strip().lower() for participant in activity["participants"]]
    if normalized_email in normalized_participants:
        raise HTTPException(status_code=400, detail="Student is already signed up for this activity")

    # Add student
    activity["participants"].append(normalized_email)
    return {"message": f"Signed up {normalized_email} for {activity_name}"}

@app.delete("/activities/{activity_name}/participants")
def remove_participant(activity_name: str, email: str):
    """Unregister a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    normalized_email = email.strip().lower()
    if not normalized_email:
        raise HTTPException(status_code=400, detail="Email is required")

    activity = activities[activity_name]
    normalized_participants = [participant.strip().lower() for participant in activity["participants"]]
    if normalized_email not in normalized_participants:
        raise HTTPException(status_code=404, detail="Participant not found")

    activity["participants"] = [participant for participant in activity["participants"] if participant.strip().lower() != normalized_email]
    return {"message": f"Removed {normalized_email} from {activity_name}"}
