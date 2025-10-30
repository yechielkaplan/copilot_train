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
    "Soccer Team": {
        "description": "Outdoor soccer training and inter-school matches",
        "schedule": "Monday to Friday, 4:00 PM - 6:00 PM",
        "max_participants": 25,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Skill development, scrimmages, and local tournaments",
        "schedule": "Tuesdays and Thursdays, 5:00 PM - 7:00 PM",
        "max_participants": 20,
        "participants": ["ava@mergington.edu", "william@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore drawing, painting, and mixed media projects",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["isabella@mergington.edu", "mia@mergington.edu"]
    },
    "Choir": {
        "description": "Vocal training, repertoire practice, and performances",
        "schedule": "Mondays, 3:30 PM - 4:30 PM",
        "max_participants": 30,
        "participants": ["sophia.j@mergington.edu", "ethan@mergington.edu"]
    },
    "Debate Team": {
        "description": "Prepare for debate competitions and practice public speaking",
        "schedule": "Mondays and Thursdays, 5:00 PM - 6:30 PM",
        "max_participants": 16,
        "participants": ["noelle@mergington.edu", "alex@mergington.edu"]
    },
    "Robotics Club": {
        "description": "Design, build, and program robots for competitions",
        "schedule": "Fridays, 3:30 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["lucas@mergington.edu", "grace@mergington.edu"]
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

    # Get the specific activity
    activity = activities[activity_name]
# Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is already signed up for this activity")
    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.post("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    # Validate student is signed up
    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Student is not registered for this activity")

    # Remove student
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
