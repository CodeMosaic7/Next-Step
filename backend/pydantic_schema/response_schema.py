from datetime import datetime,date
from pydantic import BaseModel,EmailStr,Field
from typing import Optional,List,Dict,Any
from uuid import UUID

from .core import UserProfileBase,UserSkillBase,SkillBase,PsychometricTestBase
from .Enums import AssessmentType,PriorityLevelEnum,ProficiencyLevelEnum,RoadmapStatusEnum,MilestoneStatusEnum,AgentTypeEnum,InteractionTypeEnum,BadgeCategoryEnum,BadgeRarityEnum


class UserResponse(BaseModel):
    """User response"""
    user_id: UUID
    firebase_uid: str
    email: EmailStr
    display_name: Optional[str]
    phone_number: Optional[str]
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True

class UserProfileResponse(UserProfileBase):
    """User profile response"""
    profile_id: UUID
    user_id: UUID
    psychologist_report: List[Dict[str, Any]] = Field(default_factory=list)
    counsellor_report: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class SkillResponse(SkillBase):
    """Skill response"""
    skill_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserSkillResponse(UserSkillBase):
    """User skill response"""
    user_skill_id: UUID
    user_id: UUID
    skill: SkillResponse
    is_verified: bool = False
    verification_score: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class PsychometricTestResponse(PsychometricTestBase):
    """Psychometric test response"""
    test_id: UUID
    user_id: UUID
    completion_score: float
    time_taken: Optional[int]
    taken_at: datetime
    is_complete: bool
    
    class Config:
        from_attributes = True

class AssessmentResponse(BaseModel):
    """Assessment response"""
    assessment_id: UUID
    user_id: UUID
    user_skill_id: UUID
    assessment_type: AssessmentType
    score: int
    max_score: int
    percentage: float
    time_taken: Optional[int]
    attempts_count: int
    is_passed: bool
    points_earned: int
    taken_at: datetime
    
    class Config:
        from_attributes = True

class CareerPathResponse(BaseModel):
    """Career path response"""
    path_id: UUID
    title: str
    description: Optional[str]
    industry: str
    required_skills: List[str]
    preferred_personality_traits: Dict[str, Any]
    salary_range: Dict[str, Any]
    growth_prospects: Optional[str]
    education_requirements: List[str]
    
    class Config:
        from_attributes = True

class CareerRecommendationResponse(BaseModel):
    """Career recommendation response"""
    recommendation_id: UUID
    user_id: UUID
    career_path: CareerPathResponse
    match_score: float
    reasoning: Optional[str]
    skill_gap_analysis: Dict[str, Any]
    recommended_actions: List[str]
    priority_level: PriorityLevelEnum
    is_viewed: bool
    is_bookmarked: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class RoadmapResponse(BaseModel):
    """Roadmap response"""
    roadmap_id: UUID
    user_id: UUID
    career_path_id: Optional[UUID]
    title: str
    description: Optional[str]
    target_completion_date: Optional[date]
    estimated_duration: Optional[int]
    difficulty_level: ProficiencyLevelEnum
    status: RoadmapStatusEnum
    progress_percentage: float
    created_at: datetime
    
    class Config:
        from_attributes = True

class MilestoneResponse(BaseModel):
    """Milestone response"""
    milestone_id: UUID
    roadmap_id: UUID
    title: str
    description: Optional[str]
    order_sequence: int
    estimated_duration: Optional[int]
    required_skills: List[str]
    learning_resources: List[Dict[str, Any]]
    status: MilestoneStatusEnum
    completion_date: Optional[datetime]
    points_awarded: int
    
    class Config:
        from_attributes = True

class AgentInteractionResponse(BaseModel):
    """AI agent interaction response"""
    interaction_id: UUID
    user_id: UUID
    agent_type: AgentTypeEnum
    interaction_type: InteractionTypeEnum
    user_message: str
    agent_response: str
    context_data: Dict[str, Any]
    session_token: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class GamificationProfileResponse(BaseModel):
    """Gamification profile response"""
    profile_id: UUID
    user_id: UUID
    total_points: int
    current_level: int
    experience_points: int
    badges_earned: List[Dict[str, Any]]
    achievements_unlocked: List[Dict[str, Any]]
    streak_days: int
    last_activity_date: date
    
    class Config:
        from_attributes = True

class BadgeResponse(BaseModel):
    """Badge response"""
    badge_id: UUID
    name: str
    description: Optional[str]
    icon_url: Optional[str]
    category: BadgeCategoryEnum
    points_required: int
    rarity: BadgeRarityEnum
    
    class Config:
        from_attributes = True

class UserDashboardResponse(BaseModel):
    """Complete user dashboard data"""
    user: UserResponse
    profile: Optional[UserProfileResponse]
    skills: List[UserSkillResponse]
    recent_assessments: List[AssessmentResponse]
    active_roadmaps: List[RoadmapResponse]
    career_recommendations: List[CareerRecommendationResponse]
    gamification: Optional[GamificationProfileResponse] = None
    recent_interactions: List[AgentInteractionResponse]

class PsychologistAnalysisResponse(BaseModel):
    """Psychologist agent analysis response"""
    user_id: UUID
    analysis_id: UUID
    personality_profile: Dict[str, Any]
    learning_style: Dict[str, Any]
    career_aptitude: Dict[str, Any]
    strengths: List[str]
    areas_for_development: List[str]
    recommended_career_paths: List[UUID]
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    created_at: datetime

class CounsellorRecommendationResponse(BaseModel):
    """Counsellor agent recommendation response"""
    user_id: UUID
    recommendation_id: UUID
    recommended_careers: List[CareerRecommendationResponse]
    skill_development_plan: Dict[str, Any]
    learning_roadmap: List[Dict[str, Any]]
    next_steps: List[str]
    timeline: Dict[str, Any]
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    created_at: datetime

class CoordinatorResponse(BaseModel):
    """Coordinator agent response"""
    coordination_id: UUID
    user_id: UUID
    psychologist_analysis: PsychologistAnalysisResponse
    counsellor_recommendation: CounsellorRecommendationResponse
    integrated_plan: Dict[str, Any]
    priority_actions: List[Dict[str, Any]]
    success_metrics: Dict[str, Any]
    created_at: datetime

class CompleteUserResponse(BaseModel):
    user: UserResponse
    profile: Optional[UserProfileResponse]
    profile_status: Dict[str, bool]
    registration_prompt: Optional[Dict[str, Any]] = None
