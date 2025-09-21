# auth/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from typing import Dict, Any
import uuid

# Import your existing Firebase verification
from firebase_setup import fb_verify_token

security = HTTPBearer()

class User:
    """Simple User model to match your database structure"""
    def __init__(self, user_id: str, firebase_uid: str, email: str = None, display_name: str = None):
        self.user_id = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
        self.firebase_uid = firebase_uid
        self.email = email
        self.display_name = display_name

def get_current_user(user_data: Dict[str, Any] = Depends(fb_verify_token)) -> User:
    """
    Get current user from Firebase token verification
    This replaces the auth.dependencies.get_current_user import in your routes
    """
    try:
        firebase_uid = user_data["uid"]
        email = user_data.get("email", "")
        display_name = user_data.get("name", "")
        
        # For now, use Firebase UID as user_id
        # In production, you'd want to map this to your database user_id
        user_id = firebase_uid
        
        return User(
            user_id=user_id,
            firebase_uid=firebase_uid,
            email=email,
            display_name=display_name
        )
        
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: missing {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Alternative dependency for routes that need database session
def get_current_user_with_db():
    """
    Factory function for getting current user with database integration
    Use this when you implement proper user database lookup
    """
    def _get_current_user_with_db(
        user_data: Dict[str, Any] = Depends(fb_verify_token)
        # db: Session = Depends(get_db)  # Uncomment when you have database integration
    ) -> User:
        try:
            firebase_uid = user_data["uid"]
            
            # TODO: Replace with actual database lookup
            # user = db.query(UserModel).filter(UserModel.firebase_uid == firebase_uid).first()
            # if not user:
            #     raise HTTPException(status_code=404, detail="User not found in database")
            
            # For now, create user from Firebase data
            return User(
                user_id=firebase_uid,  # Use Firebase UID as temp user_id
                firebase_uid=firebase_uid,
                email=user_data.get("email", ""),
                display_name=user_data.get("name", "")
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving user: {str(e)}"
            )
    
    return _get_current_user_with_db

# Optional: Admin-only dependency
def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency for admin-only routes
    Modify this based on how you determine admin users
    """
    # TODO: Implement admin role checking
    # For now, allow all users (modify this based on your admin logic)
    return current_user

def get_optional_user(user_data: Dict[str, Any] = Depends(fb_verify_token)) -> User | None:
    """
    Optional user dependency - returns None if no valid token
    Useful for routes that work for both authenticated and anonymous users
    """
    try:
        return get_current_user(user_data)
    except HTTPException:
        return None