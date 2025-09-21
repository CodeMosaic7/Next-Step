from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import datetime
import os
from dotenv import load_dotenv
from firebase_admin import firestore
from database.primary_db import init_db
from firebase_setup import fb_verify_token
from pydantic_schema.request_schemas import UserRegistrationRequest, UserProfileCreateRequest, UserProfileUpdateRequest
from pydantic_schema.response_schema import UserResponse, UserProfileResponse, UserDashboardResponse, CompleteUserResponse
from database.db_dependies import get_db
from routes.bot_routes import router as bot_routes
from sqlalchemy.orm import Session
from models.career_model import User, UserProfile  # Your existing models adapted for SQLite
import uuid
from sqlalchemy import create_engine
import json
import base64

load_dotenv()

origins=['http://localhost:5173']

db=firestore.client()
app = FastAPI(title="Next-Step Backend")
app.include_router(bot_routes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Next-Step Backend!"}

@app.on_event("startup")
def startup_event():
    # init DB (create tables if they don't exist)
    init_db()

    # Initialize Firebase Admin if service account provided
    sa_env = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
    if sa_env:
        try:
            # If provided base64-encoded, decode first
            try:
                decoded = base64.b64decode(sa_env).decode()
                cred_dict = json.loads(decoded)
            except Exception:
                # assume it's a JSON string
                cred_dict = json.loads(sa_env)
            import firebase_admin
            from firebase_admin import credentials
            if not firebase_admin._apps:
                credentials_obj = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(credentials_obj)
        except Exception as e:
            # log if needed — don't crash startup for prototype
            print("Warning: Firebase init failed:", e)


def get_or_create_user(user_data: dict, db_session: Session):
    """
    Get existing user or create new user from Firebase token data (SQLite compatible)
    """
    firebase_uid = user_data["uid"]
    email = user_data.get("email", "")
    
    # Check if user exists in SQLite
    existing_user = db_session.query(User).filter(User.firebase_uid == firebase_uid).first()
    
    if existing_user:
        # Update last login
        existing_user.last_login = datetime.datetime.now()
        db_session.commit()
        return existing_user
    
    # Create new user - SQLite will handle UUID generation
    new_user = User(
        firebase_uid=firebase_uid,
        email=email,
        display_name=user_data.get("name", ""),
        created_at=datetime.datetime.now(),
        last_login=datetime.datetime.now(),
        meta_data={
            "firebase_data": {
                "email_verified": user_data.get("email_verified", False),
                "sign_in_provider": user_data.get("firebase", {}).get("sign_in_provider", ""),
                "auth_time": user_data.get("auth_time", 0)
            }
        }
    )
    
    try:
        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)
        return new_user
    except Exception as e:
        db_session.rollback()
        raise Exception(f"Error creating user: {str(e)}")

def check_user_profile_completion(user: User, db_session: Session):
    """
    Check if user has completed their profile
    """
    # Access the first profile from the profiles relationship
    profile = user.profiles[0] if user.profiles else None
    
    if not profile:
        return False, None
    
    # Define required fields for a complete profile
    required_fields = ['age', 'education_level', 'current_occupation']
    missing_fields = []
    
    for field in required_fields:
        if not getattr(profile, field):
            missing_fields.append(field)
    
    is_complete = len(missing_fields) == 0
    return is_complete, profile

@app.get("/protected") #works
def protected_route(
    user_data: dict = Depends(fb_verify_token),
    db_session: Session = Depends(get_db)
):
    """
    Enhanced protected route that manages user creation and profile completion
    """
    print("Firebase user data:", user_data)
    
    try:
        # Get or create user in SQLite
        user = get_or_create_user(user_data, db_session)
        
        # Check profile completion
        is_profile_complete, profile = check_user_profile_completion(user, db_session)
        
        # Prepare response based on profile status
        response_data = {
            "message": "Hello, secure world!",
            "user": {
                "user_id": str(user.user_id),
                "firebase_uid": user.firebase_uid,
                "email": user.email,
                "display_name": user.display_name,
                "last_login": user.last_login.isoformat() if user.last_login else None
            },
            "profile_status": {
                "is_complete": is_profile_complete,
                "needs_registration": not is_profile_complete
            }
        }
        
        # If profile exists, include profile data
        if profile:
            response_data["profile"] = {
                "profile_id": str(profile.profile_id),
                "age": profile.age,
                "education_level": profile.education_level,
                "current_occupation": profile.current_occupation,
                "years_of_experience": profile.years_of_experience,
                "location": profile.location,
                "bio": profile.bio,
                "interests": profile.interests,
                "career_goals": profile.career_goals,
                "preferred_industries": profile.preferred_industries
            }
        
        # Add registration prompt if needed
        if not is_profile_complete:
            response_data["registration_prompt"] = {
                "message": "Please complete your profile to access all features",
                "redirect_to": "/registration",
                "required_fields": ["age", "education_level", "current_occupation"]
            }
        
        return response_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing user data: {str(e)}")

@app.post("/registration", response_model=UserDashboardResponse) #works
def register_route(
    registration_data: UserRegistrationRequest,
    user_data: dict = Depends(fb_verify_token),
    db_session: Session = Depends(get_db)
):
    """
    Enhanced registration that creates/updates both Firestore and SQLite records
    """
    try:
        # Get or create user in SQLite
        user = get_or_create_user(user_data, db_session)
        
        # Check if profile already exists
        existing_profile = user.profiles[0] if user.profiles else None
        
        if existing_profile:
            # Update existing profile
            existing_profile.age = registration_data.age
            existing_profile.education_level = registration_data.education_level
            existing_profile.updated_at = datetime.datetime.now()
            # Add other fields as needed
            db_session.commit()
            profile = existing_profile
        else:
            # Create new profile
            new_profile = UserProfile(
                user_id=user.user_id,
                age=registration_data.age,
                education_level=registration_data.education_level,
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now()
            )
            db_session.add(new_profile)
            db_session.commit()
            db_session.refresh(new_profile)
            profile = new_profile
        
        # Update user data from registration
        user.display_name = registration_data.display_name
        user.phone_number = registration_data.phone_number
        user.email = registration_data.email
        
        db_session.commit()
        
        # Keep Firestore logic for compatibility
        user_id = user_data["uid"]
        user_doc_data = {
            'display_name': registration_data.display_name,
            'phone_number': registration_data.phone_number,
            'user_id': user_id,
            'email': registration_data.email,
            'firebase_uid': registration_data.firebase_uid,
            'is_registered': True,
            'registered_at': firestore.SERVER_TIMESTAMP,
            'updated_at': firestore.SERVER_TIMESTAMP,
            'profile_complete': profile is not None,
            'sqlite_user_id': str(user.user_id)  # Link to SQLite record
        }
        
        db.collection('users').document(user_id).set(user_doc_data, merge=True)
        
        # Log registration
        db.collection('registration_logs').add({
            'user_id': user_id,
            'sqlite_user_id': str(user.user_id),
            'action': 'user_registered_enhanced',
            'timestamp': firestore.SERVER_TIMESTAMP,
            'data': {
                'display_name': registration_data.display_name,
                'firebase_uid': registration_data.firebase_uid
            }
        })
        
        # Create response using your schema
        user_response = UserResponse(
            user_id=user.user_id,
            firebase_uid=user.firebase_uid,
            email=user.email,
            display_name=user.display_name,
            phone_number=user.phone_number,
            created_at=user.created_at,
            last_login=user.last_login
        )
        
        profile_response = None
        if profile:
            profile_response = UserProfileResponse(
                profile_id=profile.profile_id,
                user_id=profile.user_id,
                age=profile.age,
                education_level=profile.education_level,
                current_occupation=profile.current_occupation,
                years_of_experience=profile.years_of_experience,
                location=profile.location,
                bio=profile.bio,
                interests=profile.interests or [],
                career_goals=profile.career_goals,
                preferred_industries=profile.preferred_industries or [],
                psychologist_report=profile.psychologist_report or [],
                counsellor_report=profile.counsellor_report or [],
                created_at=profile.created_at,
                updated_at=profile.updated_at
            )
        
        return UserDashboardResponse(
            user=user_response,
            profile=profile_response,
            skills=[],  # Will be populated when skills are added
            recent_assessments=[],
            active_roadmaps=[],
            career_recommendations=[],
            gamification=None,  # Will be created separately
            recent_interactions=[]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@app.get("/user/profile")
def get_user_profile(
    user_data: dict = Depends(fb_verify_token),
    db_session: Session = Depends(get_db)
):
    """
    Get complete user profile from SQLite
    """
    try:
        user = get_or_create_user(user_data, db_session)
        profile = user.profile  # Using simplified relationship
        
        response_data = {
            "user": {
                "user_id": str(user.user_id),
                "firebase_uid": user.firebase_uid,
                "email": user.email,
                "display_name": user.display_name,
                "phone_number": user.phone_number,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "last_login": user.last_login.isoformat() if user.last_login else None
            }
        }
        
        if profile:
            response_data["profile"] = {
                "profile_id": str(profile.profile_id),
                "age": profile.age,
                "education_level": profile.education_level,
                "current_occupation": profile.current_occupation,
                "years_of_experience": profile.years_of_experience,
                "location": profile.location,
                "bio": profile.bio,
                "interests": profile.interests,
                "career_goals": profile.career_goals,
                "preferred_industries": profile.preferred_industries,
                "created_at": profile.created_at.isoformat() if profile.created_at else None,
                "updated_at": profile.updated_at.isoformat() if profile.updated_at else None
            }
        else:
            response_data["profile"] = None
            response_data["message"] = "Profile not found. Please complete registration."
        
        return response_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve profile: {str(e)}")

# Keep existing endpoints for backward compatibility
@app.get("/registration")
def get_current_user_registration(
    current_user: dict = Depends(fb_verify_token)
):
    """
    Get registration data for the current authenticated user (Firestore)
    """
    try:
        user_id = current_user["uid"]
        
        user_doc = db.collection('users').document(user_id).get()
        
        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="User registration not found")
        
        user_data = user_doc.to_dict()
        
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

@app.get("/registration/status")
def check_registration_status(
    current_user: dict = Depends(fb_verify_token),
    db_session: Session = Depends(get_db)
):
    """
    Enhanced registration status check using both databases
    """
    try:
        user_id = current_user["uid"]
        
        # Check PostgreSQL
        user = get_or_create_user(current_user, db_session)
        is_profile_complete, profile = check_user_profile_completion(user, db_session)
        
        # Check Firestore for backward compatibility
        user_doc = db.collection('users').document(user_id).get()
        firestore_data = user_doc.to_dict() if user_doc.exists else {}
        
        return {
            "user_id": user_id,
            "sqlite_user_id": str(user.user_id),
            "is_registered": is_profile_complete,
            "profile_complete": is_profile_complete,
            "has_sqlite_profile": profile is not None,
            "has_firestore_data": user_doc.exists,
            "profile_fields": {
                "has_name": bool(user.display_name),
                "has_phone": bool(user.phone_number),
                "has_age": bool(profile.age if profile else False),
                "has_education": bool(profile.education_level if profile else False),
                "has_occupation": bool(profile.current_occupation if profile else False)
            },
            "message": "Registration status retrieved successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check registration status: {str(e)}")

# Profile management endpoints
@app.post("/profile", response_model=UserProfileResponse)
def create_user_profile(
    profile_data: UserProfileCreateRequest,
    user_data: dict = Depends(fb_verify_token),
    db_session: Session = Depends(get_db)
):
    """
    Create user profile after registration
    """
    try:
        user = get_or_create_user(user_data, db_session)
        
        # Check if profile already exists
        existing_profile = user.profile[0] if user.profiles else None
        
        if existing_profile:
            raise HTTPException(status_code=400, detail="Profile already exists. Use PUT to update.")
        
        # Create new profile
        new_profile = UserProfile(
            user_id=user.user_id,
            age=profile_data.age,
            education_level=profile_data.education_level,
            current_occupation=profile_data.current_occupation,
            years_of_experience=profile_data.years_of_experience,
            location=profile_data.location,
            bio=profile_data.bio,
            interests=profile_data.interests or [],
            career_goals=profile_data.career_goals,
            preferred_industries=profile_data.preferred_industries or [],
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )
        
        db_session.add(new_profile)
        db_session.commit()
        db_session.refresh(new_profile)
        
        return UserProfileResponse(
            profile_id=new_profile.profile_id,
            user_id=new_profile.user_id,
            age=new_profile.age,
            education_level=new_profile.education_level,
            current_occupation=new_profile.current_occupation,
            years_of_experience=new_profile.years_of_experience,
            location=new_profile.location,
            bio=new_profile.bio,
            interests=new_profile.interests or [],
            career_goals=new_profile.career_goals,
            preferred_industries=new_profile.preferred_industries or [],
            psychologist_report=new_profile.psychologist_report or [],
            counsellor_report=new_profile.counsellor_report or [],
            created_at=new_profile.created_at,
            updated_at=new_profile.updated_at
        )
        
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create profile: {str(e)}")

@app.put("/profile", response_model=UserProfileResponse)
def update_user_profile(
    profile_data: UserProfileUpdateRequest,
    user_data: dict = Depends(fb_verify_token),
    db_session: Session = Depends(get_db)
):
    """
    Update user profile
    """
    try:
        user = get_or_create_user(user_data, db_session)
        profile = user.profile[0] if user.profiles else None        
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found. Create profile first.")
        
        # Update only provided fields
        update_data = profile_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(profile, field):
                setattr(profile, field, value)
        
        profile.updated_at = datetime.datetime.now()
        db_session.commit()
        db_session.refresh(profile)
        
        return UserProfileResponse(
            profile_id=profile.profile_id,
            user_id=profile.user_id,
            age=profile.age,
            education_level=profile.education_level,
            current_occupation=profile.current_occupation,
            years_of_experience=profile.years_of_experience,
            location=profile.location,
            bio=profile.bio,
            interests=profile.interests or [],
            career_goals=profile.career_goals,
            preferred_industries=profile.preferred_industries or [],
            psychologist_report=profile.psychologist_report or [],
            counsellor_report=profile.counsellor_report or [],
            created_at=profile.created_at,
            updated_at=profile.updated_at
        )
        
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update profile: {str(e)}")

@app.get("/dashboard", response_model=UserDashboardResponse)
def get_user_dashboard(
    user_data: dict = Depends(fb_verify_token),
    db_session: Session = Depends(get_db)
):
    """
    Get complete user dashboard data
    """
    try:
        user = get_or_create_user(user_data, db_session)
        profile = user.profiles[0] if user.profiles else None        
        # Create user response
        user_response = UserResponse(
            user_id=user.user_id,
            firebase_uid=user.firebase_uid,
            email=user.email,
            display_name=user.display_name,
            phone_number=user.phone_number,
            created_at=user.created_at,
            last_login=user.last_login
        )
        
        # Create profile response if exists
        profile_response = None
        if profile:
            profile_response = UserProfileResponse(
                profile_id=profile.profile_id,
                user_id=profile.user_id,
                age=profile.age,
                education_level=profile.education_level,
                current_occupation=profile.current_occupation,
                years_of_experience=profile.years_of_experience,
                location=profile.location,
                bio=profile.bio,
                interests=profile.interests or [],
                career_goals=profile.career_goals,
                preferred_industries=profile.preferred_industries or [],
                psychologist_report=profile.psychologist_report or [],
                counsellor_report=profile.counsellor_report or [],
                created_at=profile.created_at,
                updated_at=profile.updated_at
            )
        
        return UserDashboardResponse(
            user=user_response,
            profile=profile_response,
            skills=[],  # TODO: Fetch user skills
            recent_assessments=[],  # TODO: Fetch recent assessments
            active_roadmaps=[],  # TODO: Fetch active roadmaps
            career_recommendations=[],  # TODO: Fetch career recommendations
            gamification=None,  # TODO: Fetch gamification profile
            recent_interactions=[]  # TODO: Fetch recent AI interactions
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get dashboard: {str(e)}")