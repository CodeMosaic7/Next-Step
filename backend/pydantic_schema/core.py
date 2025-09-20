from pydantic import BaseModel,field_validator,EmailStr
from typing import Optional,Field,List,Dict,Any
from uuid import UUID

from Enums import PriorityLevelEnum, ProficiencyLevelEnum,TestTypeEnum,AssessmentTypeEnum

class UserBase(BaseModel):
    email: EmailStr
    display_name: Optional[str] = None
    phone_number: Optional[str] = None

class UserProfileBase(BaseModel):
    age: Optional[int] = Field(None, ge=13, le=100)
    education_level: Optional[str] = None
    current_occupation: Optional[str] = None
    years_of_experience: Optional[int] = Field(0, ge=0)
    location: Optional[str] = None
    bio: Optional[str] = Field(None, max_length=1000)
    interests: List[str] = Field(default_factory=list)
    career_goals: Optional[str] = Field(None, max_length=2000)
    preferred_industries: List[str] = Field(default_factory=list)

class SkillBase(BaseModel):
    skill_name: str = Field(..., min_length=1, max_length=100)
    category: str = Field(..., min_length=1)
    description: Optional[str] = None
    industry_relevance: List[str] = Field(default_factory=list)

class UserSkillBase(BaseModel):
    skill_id: UUID
    proficiency_level: ProficiencyLevelEnum
    years_of_experience: int = Field(0, ge=0)

class PsychometricTestBase(BaseModel):
    test_type: TestTypeEnum
    results: Dict[str, Any]
    personality_traits: Dict[str, Any] = Field(default_factory=dict)
    career_preferences: Dict[str, Any] = Field(default_factory=dict)
    learning_preferences: Dict[str, Any] = Field(default_factory=dict)

class AssessmentBase(BaseModel):
    user_skill_id: UUID
    assessment_type: AssessmentTypeEnum = AssessmentTypeEnum.SKILL_TEST
    score: int = Field(..., ge=0)
    max_score: int = Field(..., ge=1)
    time_taken: Optional[int] = Field(None, ge=0)

    @field_validator('score')
    def score_not_exceed_max(cls, v, values):
        if 'max_score' in values and v > values['max_score']:
            raise ValueError('Score cannot exceed max_score')
        return v






