from datetime import datetime
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, and_, or_, func
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict,List,Optional
import uuid 

from models.career_model import (
    User, UserProfile, CareerRecommendation, CareerPath, 
    AgentInteraction, GamificationProfile, UserBadge, Badge,
    PsychometricTest, Skills, UserSkills
)
from pydantic_schema.Enums import AssessmentType


class DatabaseService:
    """Handles all database operations for the coordinator system"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    async def store_agent_interaction(self, user_id: str, agent_type: str, 
                                    interaction_type: str, user_message: str, 
                                    agent_response: str, context_data: Dict) -> str:
        """Store agent interaction in database"""
        try:
            interaction = AgentInteraction(
                user_id=uuid.UUID(user_id),
                agent_type=agent_type,
                interaction_type=interaction_type,
                user_message=user_message,
                agent_response=agent_response,
                context_data=context_data,
                session_token=str(uuid.uuid4())
            )
            
            self.db.add(interaction)
            self.db.commit()
            self.db.refresh(interaction)
            
            return str(interaction.interaction_id)
            
        except Exception as e:
            self.db.rollback()
            print(f"Error storing agent interaction: {e}")
            return None
    
    async def update_user_profile_reports(self, user_id: str, 
                                        psychologist_report: Dict, 
                                        counsellor_report: Dict):
        """Update user profile with psychological and career reports"""
        try:
            # Get or create user profile
            profile = self.db.query(UserProfile).filter(
                UserProfile.user_id == uuid.UUID(user_id)
            ).first()
            
            if not profile:
                profile = UserProfile(
                    user_id=uuid.UUID(user_id),
                    psychologist_report=psychologist_report,
                    counsellor_report=counsellor_report
                )
                self.db.add(profile)
            else:
                profile.psychologist_report = psychologist_report
                profile.counsellor_report = counsellor_report
                profile.updated_at = datetime.now()
            
            self.db.commit()
            self.db.refresh(profile)
            return str(profile.profile_id)
            
        except Exception as e:
            self.db.rollback()
            print(f"Error updating user profile reports: {e}")
            return None
    
    async def create_career_recommendations(self, user_id: str, 
                                          recommendations: List[Dict]) -> List[str]:
        """Create career recommendations based on counsellor analysis"""
        recommendation_ids = []
        
        try:
            for rec in recommendations:
                # Check if career path exists, create if not
                career_path = await self._get_or_create_career_path(rec.get('career_path', {}))
                
                recommendation = CareerRecommendation(
                    user_id=uuid.UUID(user_id),
                    career_path_id=career_path.path_id if career_path else None,
                    match_score=rec.get('match_score', 0.0),
                    reasoning=rec.get('reasoning', ''),
                    skill_gap_analysis=rec.get('skill_gap_analysis', {}),
                    recommended_actions=rec.get('recommended_actions', []),
                    priority_level=rec.get('priority_level', 'medium')
                )
                
                self.db.add(recommendation)
                self.db.commit()
                self.db.refresh(recommendation)
                recommendation_ids.append(str(recommendation.recommendation_id))
            
            return recommendation_ids
            
        except Exception as e:
            self.db.rollback()
            print(f"Error creating career recommendations: {e}")
            return []
    
    async def _get_or_create_career_path(self, career_data: Dict) -> Optional[CareerPath]:
        """Get existing or create new career path"""
        if not career_data.get('title'):
            return None
            
        try:
            # Check if career path exists
            existing_path = self.db.query(CareerPath).filter(
                CareerPath.title == career_data['title']
            ).first()
            
            if existing_path:
                return existing_path
            
            # Create new career path
            career_path = CareerPath(
                title=career_data['title'],
                description=career_data.get('description', ''),
                industry=career_data.get('industry', 'General'),
                required_skills=career_data.get('required_skills', []),
                preferred_personality_traits=career_data.get('personality_traits', {}),
                salary_range=career_data.get('salary_range', {}),
                growth_prospects=career_data.get('growth_prospects', ''),
                education_requirements=career_data.get('education_requirements', []),
                experience_requirements=career_data.get('experience_requirements', '')
            )
            
            self.db.add(career_path)
            self.db.commit()
            self.db.refresh(career_path)
            
            return career_path
            
        except Exception as e:
            print(f"Error creating career path: {e}")
            return None
    
    async def store_psychometric_insights(self, user_id: str, 
                                        assessment_type: AssessmentType,
                                        insights: Dict) -> str:
        """Store psychometric insights as a test result"""
        try:
            psychometric_test = PsychometricTest(
                user_id=uuid.UUID(user_id),
                test_type=assessment_type.value,
                results=insights.get('raw_results', {}),
                personality_traits=insights.get('personality_traits', {}),
                career_preferences=insights.get('career_preferences', {}),
                learning_preferences=insights.get('learning_preferences', {}),
                completion_score=insights.get('completion_score', 100.0),
                is_complete=True
            )
            
            self.db.add(psychometric_test)
            self.db.commit()
            self.db.refresh(psychometric_test)
            
            return str(psychometric_test.test_id)
            
        except Exception as e:
            self.db.rollback()
            print(f"Error storing psychometric insights: {e}")
            return None
    
    async def update_user_skills_from_analysis(self, user_id: str, 
                                             identified_skills: List[Dict]):
        """Update user skills based on psychological and career analysis"""
        try:
            for skill_data in identified_skills:
                skill_name = skill_data.get('skill_name')
                if not skill_name:
                    continue
                
                # Get or create skill
                skill = await self._get_or_create_skill(skill_data)
                if not skill:
                    continue
                
                # Check if user already has this skill
                existing_user_skill = self.db.query(UserSkills).filter(
                    and_(
                        UserSkills.user_id == uuid.UUID(user_id),
                        UserSkills.skill_id == skill.skill_id
                    )
                ).first()
                
                if existing_user_skill:
                    # Update existing skill if confidence is higher
                    if skill_data.get('proficiency_level'):
                        existing_user_skill.proficiency_level = skill_data['proficiency_level']
                        existing_user_skill.updated_at = datetime.now()
                else:
                    # Create new user skill
                    user_skill = UserSkills(
                        user_id=uuid.UUID(user_id),
                        skill_id=skill.skill_id,
                        proficiency_level=skill_data.get('proficiency_level', 'beginner'),
                        is_verified=False  # Since it's from assessment analysis
                    )
                    self.db.add(user_skill)
            
            self.db.commit()
            
        except Exception as e:
            self.db.rollback()
            print(f"Error updating user skills: {e}")
    
    async def _get_or_create_skill(self, skill_data: Dict) -> Optional[Skills]:
        """Get existing or create new skill"""
        skill_name = skill_data.get('skill_name')
        if not skill_name:
            return None
            
        try:
            # Check if skill exists
            existing_skill = self.db.query(Skills).filter(
                Skills.skill_name.ilike(f"%{skill_name}%")
            ).first()
            
            if existing_skill:
                return existing_skill
            
            # Create new skill
            skill = Skills(
                skill_name=skill_name,
                category=skill_data.get('category', 'general'),
                description=skill_data.get('description', ''),
                industry_relevance=skill_data.get('industry_relevance', [])
            )
            
            self.db.add(skill)
            self.db.commit()
            self.db.refresh(skill)
            
            return skill
            
        except Exception as e:
            print(f"Error creating skill: {e}")
            return None
    
    async def award_points_and_badges(self, user_id: str, activity_type: str, 
                                    points: int = 0) -> Dict:
        """Award points and check for new badges"""
        try:
            # Get or create gamification profile
            gamification_profile = self.db.query(GamificationProfile).filter(
                GamificationProfile.user_id == uuid.UUID(user_id)
            ).first()
            
            if not gamification_profile:
                gamification_profile = GamificationProfile(
                    user_id=uuid.UUID(user_id),
                    total_points=points,
                    experience_points=points
                )
                self.db.add(gamification_profile)
            else:
                gamification_profile.total_points += points
                gamification_profile.experience_points += points
            
            # Update level based on experience points
            new_level = self._calculate_level(gamification_profile.experience_points)
            level_up = new_level > gamification_profile.current_level
            gamification_profile.current_level = new_level
            
            # Check for new badges
            new_badges = await self._check_and_award_badges(user_id, activity_type, gamification_profile)
            
            self.db.commit()
            
            return {
                "points_awarded": points,
                "total_points": gamification_profile.total_points,
                "new_level": new_level,
                "level_up": level_up,
                "new_badges": new_badges
            }
            
        except Exception as e:
            self.db.rollback()
            print(f"Error awarding points and badges: {e}")
            return {}
    
    def _calculate_level(self, experience_points: int) -> int:
        """Calculate user level based on experience points"""
        # Simple leveling formula: level = floor(sqrt(experience_points / 100))
        import math
        return max(1, int(math.sqrt(experience_points / 100)))
    
    async def _check_and_award_badges(self, user_id: str, activity_type: str, 
                                    profile: GamificationProfile) -> List[Dict]:
        """Check and award new badges"""
        new_badges = []
        
        try:
            # Define badge criteria based on activity
            badge_criteria = {
                'assessment_completion': {'points_threshold': 50, 'badge_name': 'Assessment Explorer'},
                'career_guidance': {'points_threshold': 100, 'badge_name': 'Career Seeker'},
                'psychological_analysis': {'points_threshold': 75, 'badge_name': 'Self-Aware'}
            }
            
            criteria = badge_criteria.get(activity_type, {})
            if not criteria:
                return new_badges
            
            # Check if user meets criteria and doesn't have badge yet
            if profile.total_points >= criteria['points_threshold']:
                badge = self.db.query(Badge).filter(
                    Badge.name == criteria['badge_name']
                ).first()
                
                if badge:
                    # Check if user already has this badge
                    existing_user_badge = self.db.query(UserBadge).filter(
                        and_(
                            UserBadge.user_id == uuid.UUID(user_id),
                            UserBadge.badge_id == badge.badge_id
                        )
                    ).first()
                    
                    if not existing_user_badge:
                        # Award the badge
                        user_badge = UserBadge(
                            user_id=uuid.UUID(user_id),
                            badge_id=badge.badge_id
                        )
                        self.db.add(user_badge)
                        
                        new_badges.append({
                            'name': badge.name,
                            'description': badge.description,
                            'rarity': badge.rarity
                        })
            
            return new_badges
            
        except Exception as e:
            print(f"Error checking badges: {e}")
            return []
