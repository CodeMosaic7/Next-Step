from pydantic import BaseModel
from typing import Field, Optional, List, Any
from Enums import PriorityLevelEnum, AssessmentTypeEnum,ProficiencyLevelEnum
from datetime import date

class PaginationParams(BaseModel):
    """Pagination parameters"""
    page: int = Field(1, ge=1)
    size: int = Field(20, ge=1, le=100)
    
class PaginatedResponse(BaseModel):
    """Generic paginated response"""
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int
    
    class Config:
        arbitrary_types_allowed = True

class SkillFilterParams(BaseModel):
    """Skill filtering parameters"""
    category: Optional[str] = None
    industry: Optional[str] = None
    proficiency_level: Optional[ProficiencyLevelEnum] = None
    search: Optional[str] = None

class AssessmentFilterParams(BaseModel):
    """Assessment filtering parameters"""
    assessment_type: Optional[AssessmentTypeEnum] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    is_passed: Optional[bool] = None
