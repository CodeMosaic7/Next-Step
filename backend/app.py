from fastapi import FastAPI, Depends,HTTPException
from fastapi.middleware.cors import CORSMiddleware
import datetime
import os
from dotenv import load_dotenv
from firebase_admin import firestore
from database.primary_db import init_db
from firebase_setup import fb_verify_token
from pydantic_schema import RegistrationData
from database.db_dependies import get_db
from .routes.bot_routes import router as bot_routes
load_dotenv()

origins=['http://localhost:5173']

db=firestore.client()
app = FastAPI(title="Next-Step Backend")
app.include_router(bot_routes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         # who can talk to your backend
    allow_credentials=True,        # allow cookies/auth
    allow_methods=["*"],           # allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],           # allow all headers (like Authorization)
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Next-Step Backend!"}

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/protected")
def protected_route(user_data: dict = Depends(fb_verify_token)):
    return {"message": "Hello, secure world!", "user": user_data["uid"]}

@app.post("/registration")
def register_route(
    registration_data: RegistrationData,
    user_data: dict = Depends(fb_verify_token)
):
    """
    Register a user with their personal information
    Requires authentication via Firebase token
    """
    try:
        # Extract user ID from authenticated user
        user_id = user_data["uid"]
        
        # Check if user is already registered
        existing_registration = db.collection('users').document(user_id).get()
        if existing_registration.exists and existing_registration.to_dict().get('is_registered', False):
            raise HTTPException(status_code=400, detail="User is already registered")
        
        # Prepare user data for Firestore
        user_doc_data = {
            'name': registration_data.name,
            'age': registration_data.age,
            'education_level': registration_data.education_level,
            'phone_no': registration_data.phone_no,
            'user_id': user_id,
            'email': user_data.get('email', ''),  # Get email from Firebase auth token
            'is_registered': True,
            'registered_at': firestore.SERVER_TIMESTAMP,
            'updated_at': firestore.SERVER_TIMESTAMP,
            'profile_complete': True
        }
        
        # Save registration data to Firestore
        db.collection('users').document(user_id).set(user_doc_data, merge=True)
        
        # Optionally, also create a separate registration log
        db.collection('registration_logs').add({
            'user_id': user_id,
            'action': 'user_registered',
            'timestamp': firestore.SERVER_TIMESTAMP,
            'data': {
                'name': registration_data.name,
                'education_level': registration_data.education_level
            }
        })
        
        return {
            "message": "Registered Successfully",
            "user_id": user_id,
            "registration_data": {
                "name": registration_data.name,
                "age": registration_data.age,
                "education_level": registration_data.education_level,
                "phone_no": registration_data.phone_no,
                "email": user_data.get('email', ''),
                "registered_at": datetime.now().isoformat()
            }
        }
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

# Get user registration data endpoint
@app.get("/registration")
def get_current_user_registration(
    current_user: dict = Depends(fb_verify_token)
):
    """
    Get registration data for the current authenticated user
    """
    try:
        user_id = current_user["uid"]
        
        # Fetch user data from Firestore
        user_doc = db.collection('users').document(user_id).get()
        
        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="User registration not found")
        
        user_data = user_doc.to_dict()
        
        # Remove sensitive server fields from response
        response_data = {
            "name": user_data.get("name"),
            "age": user_data.get("age"),
            "education_level": user_data.get("education_level"),
            "phone_no": user_data.get("phone_no"),
            "email": user_data.get("email"),
            "is_registered": user_data.get("is_registered", False),
            "profile_complete": user_data.get("profile_complete", False),
            "registered_at": user_data.get("registered_at")
        }
        
        return {
            "message": "Registration data retrieved successfully",
            "user_id": user_id,
            "data": response_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve registration: {str(e)}")

# Update user registration data
@app.put("/registration")
def update_registration(
    registration_data: RegistrationData,
    current_user: dict = Depends(fb_verify_token)
):
    """
    Update registration data for the current authenticated user
    """
    try:
        user_id = current_user["uid"]
        
        # Check if user exists
        user_doc = db.collection('users').document(user_id).get()
        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="User not found. Please register first.")
        
        # Update user data
        update_data = {
            'name': registration_data.name,
            'age': registration_data.age,
            'education_level': registration_data.education_level,
            'phone_no': registration_data.phone_no,
            'updated_at': firestore.SERVER_TIMESTAMP,
            'profile_complete': True
        }
        
        db.collection('users').document(user_id).update(update_data)
        
        # Log the update
        db.collection('registration_logs').add({
            'user_id': user_id,
            'action': 'registration_updated',
            'timestamp': firestore.SERVER_TIMESTAMP,
            'data': {
                'name': registration_data.name,
                'education_level': registration_data.education_level
            }
        })
        
        return {
            "message": "Registration updated successfully",
            "user_id": user_id,
            "updated_data": {
                "name": registration_data.name,
                "age": registration_data.age,
                "education_level": registration_data.education_level,
                "phone_no": registration_data.phone_no
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update registration: {str(e)}")

# Check if user is registered
@app.get("/registration/status")
def check_registration_status(
    current_user: dict = Depends(fb_verify_token)
):
    """
    Check if the current user has completed registration
    """
    try:
        user_id = current_user["uid"]
        
        user_doc = db.collection('users').document(user_id).get()
        
        if not user_doc.exists:
            return {
                "user_id": user_id,
                "is_registered": False,
                "profile_complete": False,
                "message": "User not registered"
            }
        
        user_data = user_doc.to_dict()
        
        return {
            "user_id": user_id,
            "is_registered": user_data.get("is_registered", False),
            "profile_complete": user_data.get("profile_complete", False),
            "has_name": bool(user_data.get("name")),
            "has_phone": bool(user_data.get("phone_no")),
            "message": "Registration status retrieved successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check registration status: {str(e)}")