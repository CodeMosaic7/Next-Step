from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from uuid import UUID
import uuid
from datetime import datetime

# Import your existing modules
from app.database.db_dependies import get_db
from app.models.career_model import (
    User, UserProfile, CareerRecommendation, CareerPath, 
    AgentInteraction, GamificationProfile, UserBadge, Badge,
    PsychometricTest, Skills, UserSkills, Assessment
)

# Import Pydantic models from your documents
from app.pydantic_schema.request_schemas import (
    AgentInteractionRequest, PsychometricTestRequest, 
    AssessmentSubmitRequest, UserProfileUpdateRequest
)
from app.pydantic_schema.response_schema import (
    AgentInteractionResponse, PsychologistAnalysisResponse,
    CounsellorRecommendationResponse, CoordinatorResponse,
    UserDashboardResponse, GamificationProfileResponse
)
from app.pydantic_schema.Enums import AssessmentType, AgentTypeEnum

# Import your coordinator system
from app.agents.main import CoordinatorSystem
from app.agents.Database_service_layer import DatabaseService
from app.auth.dependencies import get_current_user  # Assuming you have auth

# Create router
router = APIRouter(prefix="/api/v1", tags=["AI Agents & Coordination"])
security = HTTPBearer()

# ============================================================================
# ASSESSMENT AND COORDINATION ROUTES
# ============================================================================

@router.post("/assessment/process", response_model=CoordinatorResponse)
async def process_assessment_report(
    assessment_id: UUID,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Process completed assessment through coordinator system"""
    try:
        # Get the assessment and its report
        assessment = db.query(Assessment).filter(
            Assessment.assessment_id == assessment_id,
            Assessment.user_id == current_user.user_id
        ).first()
        
        if not assessment:
            raise HTTPException(status_code=404, detail="Assessment not found")
        
        # Get the assessment report (assuming you have this stored)
        # This would come from your existing AssessmentBot system
        assessment_report = await get_assessment_report(assessment_id, db)
        
        if not assessment_report:
            raise HTTPException(status_code=400, detail="Assessment report not generated yet")
        
        # Process through coordinator system
        coordinator_system = CoordinatorSystem(db)
        
        result = await coordinator_system.process_assessment_report(
            user_id=str(current_user.user_id),
            assessment_report=assessment_report,
            assessment_type=AssessmentType.PSYCHOMETRIC  # Determine from assessment
        )
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        # Format response according to your Pydantic model
        return format_coordinator_response(result, current_user.user_id)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing assessment: {str(e)}")


@router.post("/agent/interact", response_model=AgentInteractionResponse)
async def interact_with_agent(
    request: AgentInteractionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Interact with AI agents (psychologist, counsellor, coordinator)"""
    try:
        coordinator_system = CoordinatorSystem(db)
        db_service = DatabaseService(db)
        
        response = ""
        
        if request.agent_type == AgentTypeEnum.PSYCHOLOGIST:
            # Direct interaction with psychologist
            response = await coordinator_system.psychologist.provide_support(
                concerns=request.user_message,
                strengths="",  # Could be retrieved from user profile
                context=str(request.context_data)
            )
            
        elif request.agent_type == AgentTypeEnum.COUNSELLOR:
            # Direct interaction with counsellor
            response = await coordinator_system.counsellor.create_development_plan(
                traits="",  # Could be retrieved from user profile
                career_paths="",  # Could be retrieved from recommendations
                context=request.user_message
            )
            
        elif request.agent_type == AgentTypeEnum.COORDINATOR:
            # Handle coordinator interactions (like follow-ups)
            if request.session_token:
                response = await coordinator_system.provide_followup_support(
                    user_id=str(current_user.user_id),
                    session_id=request.session_token,
                    followup_question=request.user_message
                )
            else:
                response = "Please provide a session token for coordinator interactions."
        
        # Store interaction in database
        interaction_id = await db_service.store_agent_interaction(
            user_id=str(current_user.user_id),
            agent_type=request.agent_type.value,
            interaction_type=request.interaction_type.value,
            user_message=request.user_message,
            agent_response=response,
            context_data=request.context_data
        )
        
        # Return response
        return AgentInteractionResponse(
            interaction_id=UUID(interaction_id) if interaction_id else uuid.uuid4(),
            user_id=current_user.user_id,
            agent_type=request.agent_type,
            interaction_type=request.interaction_type,
            user_message=request.user_message,
            agent_response=response,
            context_data=request.context_data,
            session_token=request.session_token,
            created_at=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interacting with agent: {str(e)}")


@router.get("/user/dashboard", response_model=UserDashboardResponse)
async def get_user_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get comprehensive user dashboard with all data"""
    try:
        # Get user profile
        profile = db.query(UserProfile).filter(
            UserProfile.user_id == current_user.user_id
        ).first()
        
        # Get user skills
        skills = db.query(UserSkills).filter(
            UserSkills.user_id == current_user.user_id
        ).limit(10).all()
        
        # Get recent assessments
        recent_assessments = db.query(Assessment).filter(
            Assessment.user_id == current_user.user_id
        ).order_by(Assessment.taken_at.desc()).limit(5).all()
        
        # Get career recommendations
        career_recommendations = db.query(CareerRecommendation).filter(
            CareerRecommendation.user_id == current_user.user_id
        ).order_by(CareerRecommendation.created_at.desc()).limit(5).all()
        
        # Get gamification profile
        gamification = db.query(GamificationProfile).filter(
            GamificationProfile.user_id == current_user.user_id
        ).first()
        
        if not gamification:
            # Create default gamification profile
            gamification = GamificationProfile(
                user_id=current_user.user_id,
                total_points=0,
                current_level=1,
                experience_points=0
            )
            db.add(gamification)
            db.commit()
            db.refresh(gamification)
        
        # Get recent agent interactions
        recent_interactions = db.query(AgentInteraction).filter(
            AgentInteraction.user_id == current_user.user_id
        ).order_by(AgentInteraction.created_at.desc()).limit(10).all()
        
        # Format and return dashboard response
        return format_dashboard_response(
            current_user, profile, skills, recent_assessments,
            [], career_recommendations, gamification, recent_interactions
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching dashboard: {str(e)}")


@router.get("/user/psychological-reports")
async def get_psychological_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's psychological analysis reports"""
    try:
        profile = db.query(UserProfile).filter(
            UserProfile.user_id == current_user.user_id
        ).first()
        
        if not profile:
            return {"psychological_reports": []}
        
        # Get psychometric tests
        psychometric_tests = db.query(PsychometricTest).filter(
            PsychometricTest.user_id == current_user.user_id
        ).order_by(PsychometricTest.taken_at.desc()).all()
        
        return {
            "psychological_reports": profile.psychologist_report,
            "psychometric_tests": [
                {
                    "test_id": test.test_id,
                    "test_type": test.test_type,
                    "personality_traits": test.personality_traits,
                    "taken_at": test.taken_at,
                    "completion_score": test.completion_score
                }
                for test in psychometric_tests
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching psychological reports: {str(e)}")


@router.get("/user/career-guidance")
async def get_career_guidance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's career guidance reports"""
    try:
        profile = db.query(UserProfile).filter(
            UserProfile.user_id == current_user.user_id
        ).first()
        
        career_recommendations = db.query(CareerRecommendation).filter(
            CareerRecommendation.user_id == current_user.user_id
        ).order_by(CareerRecommendation.created_at.desc()).all()
        
        return {
            "counsellor_reports": profile.counsellor_report if profile else [],
            "career_recommendations": [
                {
                    "recommendation_id": rec.recommendation_id,
                    "career_path_id": rec.career_path_id,
                    "match_score": rec.match_score,
                    "reasoning": rec.reasoning,
                    "skill_gap_analysis": rec.skill_gap_analysis,
                    "recommended_actions": rec.recommended_actions,
                    "priority_level": rec.priority_level,
                    "created_at": rec.created_at
                }
                for rec in career_recommendations
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching career guidance: {str(e)}")


@router.post("/user/profile/update")
async def update_user_profile(
    profile_update: UserProfileUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update user profile"""
    try:
        profile = db.query(UserProfile).filter(
            UserProfile.user_id == current_user.user_id
        ).first()
        
        if not profile:
            # Create new profile
            profile = UserProfile(user_id=current_user.user_id)
            db.add(profile)
        
        # Update profile fields
        update_data = profile_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(profile, field, value)
        
        profile.updated_at = datetime.now()
        db.commit()
        db.refresh(profile)
        
        return {"message": "Profile updated successfully", "profile_id": profile.profile_id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating profile: {str(e)}")


@router.get("/gamification/profile", response_model=GamificationProfileResponse)
async def get_gamification_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's gamification profile"""
    try:
        gamification = db.query(GamificationProfile).filter(
            GamificationProfile.user_id == current_user.user_id
        ).first()
        
        if not gamification:
            # Create default profile
            gamification = GamificationProfile(
                user_id=current_user.user_id,
                total_points=0,
                current_level=1,
                experience_points=0
            )
            db.add(gamification)
            db.commit()
            db.refresh(gamification)
        
        # Get user badges
        user_badges = db.query(UserBadge).filter(
            UserBadge.user_id == current_user.user_id
        ).all()
        
        badges_earned = []
        for user_badge in user_badges:
            badge = db.query(Badge).filter(Badge.badge_id == user_badge.badge_id).first()
            if badge:
                badges_earned.append({
                    "badge_id": badge.badge_id,
                    "name": badge.name,
                    "description": badge.description,
                    "earned_at": user_badge.earned_at
                })
        
        return GamificationProfileResponse(
            profile_id=gamification.profile_id,
            user_id=gamification.user_id,
            total_points=gamification.total_points,
            current_level=gamification.current_level,
            experience_points=gamification.experience_points,
            badges_earned=badges_earned,
            achievements_unlocked=gamification.achievements_unlocked,
            streak_days=gamification.streak_days,
            last_activity_date=gamification.last_activity_date
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching gamification profile: {str(e)}")


@router.get("/agent/interactions/history")
async def get_agent_interaction_history(
    agent_type: Optional[AgentTypeEnum] = None,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's interaction history with AI agents"""
    try:
        query = db.query(AgentInteraction).filter(
            AgentInteraction.user_id == current_user.user_id
        )
        
        if agent_type:
            query = query.filter(AgentInteraction.agent_type == agent_type.value)
        
        interactions = query.order_by(
            AgentInteraction.created_at.desc()
        ).limit(limit).all()
        
        return {
            "interactions": [
                {
                    "interaction_id": interaction.interaction_id,
                    "agent_type": interaction.agent_type,
                    "interaction_type": interaction.interaction_type,
                    "user_message": interaction.user_message,
                    "agent_response": interaction.agent_response,
                    "created_at": interaction.created_at,
                    "session_token": interaction.session_token
                }
                for interaction in interactions
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching interaction history: {str(e)}")


@router.post("/assessment/trigger-coordination")
async def trigger_assessment_coordination(
    assessment_id: UUID,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Trigger coordination process for completed assessment (background task)"""
    try:
        # Verify assessment belongs to user
        assessment = db.query(Assessment).filter(
            Assessment.assessment_id == assessment_id,
            Assessment.user_id == current_user.user_id
        ).first()
        
        if not assessment:
            raise HTTPException(status_code=404, detail="Assessment not found")
        
        # Add coordination task to background
        background_tasks.add_task(
            process_assessment_coordination,
            assessment_id,
            str(current_user.user_id),
            db
        )
        
        return {
            "message": "Assessment coordination process initiated",
            "assessment_id": assessment_id,
            "status": "processing"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error triggering coordination: {str(e)}")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

async def get_assessment_report(assessment_id: UUID, db: Session) -> Optional[str]:
    """Get assessment report from your existing system"""
    # This would integrate with your existing AssessmentBot
    # For now, return a placeholder
    return """
    Sample assessment report for coordination processing.
    This would come from your existing AssessmentBot system.
    """

def format_coordinator_response(result: Dict[str, Any], user_id: UUID) -> CoordinatorResponse:
    """Format coordinator system result into response model"""
    return CoordinatorResponse(
        coordination_id=uuid.uuid4(),
        user_id=user_id,
        psychologist_analysis=PsychologistAnalysisResponse(
            user_id=user_id,
            analysis_id=uuid.uuid4(),
            personality_profile=result.get("psychological_data", {}).get("personality_traits", {}),
            learning_style={},
            career_aptitude={},
            strengths=result.get("psychological_data", {}).get("strengths", []),
            areas_for_development=[],
            recommended_career_paths=[],
            confidence_score=0.8,
            created_at=datetime.now()
        ),
        counsellor_recommendation=CounsellorRecommendationResponse(
            user_id=user_id,
            recommendation_id=uuid.uuid4(),
            recommended_careers=[],
            skill_development_plan=result.get("career_data", {}).get("action_plan", {}),
            learning_roadmap=[],
            next_steps=result.get("career_data", {}).get("action_plan", {}).get("short_term", []),
            timeline={},
            confidence_score=0.8,
            created_at=datetime.now()
        ),
        integrated_plan={
            "comprehensive_report": result.get("comprehensive_report", ""),
            "support_needs": result.get("support_needs", {})
        },
        priority_actions=[],
        success_metrics={},
        created_at=datetime.now()
    )

def format_dashboard_response(user, profile, skills, assessments, roadmaps, 
                            career_recs, gamification, interactions) -> UserDashboardResponse:
    """Format dashboard data into response model"""
    # This is a simplified implementation - you'd expand based on your needs
    return UserDashboardResponse(
        user=user,
        profile=profile,
        skills=skills[:5],  # Limit for dashboard
        recent_assessments=assessments,
        active_roadmaps=roadmaps,
        career_recommendations=career_recs,
        gamification=gamification,
        recent_interactions=interactions[:5]
    )

async def process_assessment_coordination(assessment_id: UUID, user_id: str, db: Session):
    """Background task for processing assessment coordination"""
    try:
        coordinator_system = CoordinatorSystem(db)
        
        # Get assessment report
        assessment_report = await get_assessment_report(assessment_id, db)
        
        if assessment_report:
            # Process through coordinator
            await coordinator_system.process_assessment_report(
                user_id=user_id,
                assessment_report=assessment_report,
                assessment_type=AssessmentType.PSYCHOMETRIC
            )
            
    except Exception as e:
        print(f"Background coordination error: {e}")


# Include the router in your main FastAPI app
# app.include_router(router)