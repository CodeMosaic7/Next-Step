from pydantic import BaseModel,Field
from .core import UserBase,UserProfileBase,PsychometricTestBase,AssessmentBase,UserSkillBase
from typing import Optional,List,Dict,Any
from .Enums import TestTypeEnum,ProficiencyLevelEnum,AssessmentTypeEnum,AgentTypeEnum,SessionTypeEnum,InteractionTypeEnum
from uuid import UUID
from datetime import date,datetime

class UserRegistrationRequest(UserBase):
    """Initial user registration - minimal info"""
    firebase_uid: str = Field(..., min_length=1)
    password: Optional[str] = Field(None, min_length=8)
    
    class Config:
        schema_extra = {
            "example": {
                "firebase_uid": "firebase_uid_123",
                "email": "student@example.com",
                "display_name": "John Doe",
                "phone_number": "+1234567890"
            }
        }

class UserProfileCreateRequest(UserProfileBase):
    """Profile creation after registration"""
    pass

class UserProfileUpdateRequest(BaseModel):
    """Profile update - all fields optional"""
    age: Optional[int] = Field(None, ge=13, le=100)
    education_level: Optional[str] = None
    current_occupation: Optional[str] = None
    years_of_experience: Optional[int] = Field(None, ge=0)
    location: Optional[str] = None
    bio: Optional[str] = Field(None, max_length=1000)
    interests: Optional[List[str]] = None
    career_goals: Optional[str] = Field(None, max_length=2000)
    preferred_industries: Optional[List[str]] = None

class PsychometricTestRequest(BaseModel):
    """Request to take a psychometric test"""
    test_type: TestTypeEnum
    answers: Dict[str, Any]  # Question ID -> Answer mapping
    
    class Config:
        schema_extra = {
            "example": {
                "test_type": "MBTI",
                "answers": {
                    "q1": "A",
                    "q2": "B",
                    "q3": "A"
                }
            }
        }

class PsychometricTestSubmitRequest(PsychometricTestBase):
    """Submit completed psychometric test"""
    completion_score: float = Field(0.0, ge=0.0, le=100.0)
    time_taken: Optional[int] = Field(None, ge=0)

class AssessmentCreateRequest(AssessmentBase):
    """Create new assessment"""
    questions: Optional[List[Dict[str, Any]]] = Field(default_factory=list)

class AssessmentSubmitRequest(BaseModel):
    """Submit assessment answers"""
    assessment_id: UUID
    answers: List[Dict[str, Any]]  # [{"question_id": UUID, "answer": "...", "time_taken": 30}]
    
    class Config:
        schema_extra = {
            "example": {
                "assessment_id": "123e4567-e89b-12d3-a456-426614174000",
                "answers": [
                    {
                        "question_id": "123e4567-e89b-12d3-a456-426614174001",
                        "answer": "A",
                        "time_taken": 30
                    }
                ]
            }
        }

class SkillAssessmentRequest(BaseModel):
    """Request skill assessment"""
    skill_ids: List[UUID] = Field(..., min_items=1)
    assessment_type: AssessmentTypeEnum = AssessmentTypeEnum.SKILL_TEST
    
class UserSkillCreateRequest(UserSkillBase):
    """Add skill to user profile"""
    pass

class UserSkillUpdateRequest(BaseModel):
    """Update user skill"""
    proficiency_level: Optional[ProficiencyLevelEnum] = None
    years_of_experience: Optional[int] = Field(None, ge=0)

class AgentInteractionRequest(BaseModel):
    """Request to interact with AI agent"""
    agent_type: AgentTypeEnum
    interaction_type: InteractionTypeEnum
    user_message: str = Field(..., min_length=1, max_length=5000)
    context_data: Dict[str, Any] = Field(default_factory=dict)
    session_token: Optional[str] = None

class MentorshipSessionRequest(BaseModel):
    """Request mentorship session"""
    mentor_id: UUID
    session_type: SessionTypeEnum
    scheduled_time: datetime
    duration_minutes: int = Field(..., ge=15, le=180)
    agenda: Optional[str] = Field(None, max_length=1000)

class RoadmapCreateRequest(BaseModel):
    """Create learning roadmap"""
    career_path_id: Optional[UUID] = None
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    target_completion_date: Optional[date] = None
    difficulty_level: ProficiencyLevelEnum = ProficiencyLevelEnum.INTERMEDIATE
