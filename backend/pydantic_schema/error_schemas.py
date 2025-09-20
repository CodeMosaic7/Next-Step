from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional,Field,Any
class ErrorDetail(BaseModel):
    """Error detail"""
    field: Optional[str] = None
    message: str
    code: Optional[str] = None

class ErrorResponse(BaseModel):
    """Standard error response"""
    error: bool = True
    message: str
    details: List[ErrorDetail] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SuccessResponse(BaseModel):
    """Standard success response"""
    success: bool = True
    message: str
    data: Optional[Any] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        arbitrary_types_allowed = True