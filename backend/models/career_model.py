import uuid
from datetime import datetime, date
from sqlalchemy import (
    Column, String, DateTime, Boolean, Enum, ForeignKey,
    Integer, Text, Date, UniqueConstraint, Index, Float
)
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# --- USERS ---
class User(Base):
    __tablename__ = "users"
    
    user_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    firebase_uid = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    display_name = Column(String)
    phone_number = Column(String)
    created_at = Column(DateTime, default=datetime.now, index=True)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    last_login = Column(DateTime, index=True)
    created_by_ip = Column(String)
    
    meta_data = Column(JSON, default=lambda: {})
    
    profiles = relationship("UserProfile", back_populates="user", cascade="all, delete-orphan")
    skills = relationship("UserSkills", back_populates="user", cascade="all, delete-orphan")
    user_roles = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")
    psychometric_tests = relationship("PsychometricTest", back_populates="user", cascade="all, delete-orphan")
    roadmaps = relationship("Roadmap", back_populates="user", cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="user", cascade="all, delete-orphan")
    career_recommendations = relationship("CareerRecommendation", back_populates="user", cascade="all, delete-orphan")
    gamification_profile = relationship("GamificationProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")

    # Temporarily commented out to avoid mapper initialization errors
    # mentorship_as_mentor = relationship(
    #     "MentorshipSession",
    #     back_populates="mentor",
    #     foreign_keys="MentorshipSession.mentor_id",
    #     cascade="all, delete-orphan"
    # )
    # mentorship_as_mentee = relationship(
    #     "MentorshipSession",
    #     back_populates="mentee",
    #     foreign_keys="MentorshipSession.mentee_id",
    #     cascade="all, delete-orphan"
    # )

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    profile_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False, unique=True)
    age = Column(Integer)
    education_level = Column(String)
    current_occupation = Column(String)
    years_of_experience = Column(Integer, default=0)
    location = Column(String)
    bio = Column(Text)
    
    # JSON fields for SQLite (stored as text)
    interests = Column(JSON, default=lambda: [])
    career_goals = Column(Text)
    preferred_industries = Column(JSON, default=lambda: [])
    psychologist_report = Column(JSON, default=lambda: [])
    counsellor_report = Column(JSON, default=lambda: [])
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    user = relationship("User", back_populates="profiles")

# --- ROLES ---
class Role(Base):
    __tablename__ = "roles"

    role_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_name = Column(
        Enum("admin", "mentors", "student", "career_counselor", name="role_name"),
        unique=True,
        nullable=False
    )
    description = Column(Text)
    permissions = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    user_roles = relationship("UserRole", back_populates="role")


class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # association PK
    user_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.role_id", ondelete="CASCADE"), nullable=False)
    role_name = Column(String, nullable=False)  # redundant, but okay if you need quick access
    granted_at = Column(DateTime, default=datetime.now)
    granted_by = Column(String)  # admin user_id who granted this role

    # Relationships
    user = relationship("User", back_populates="user_roles")
    role = relationship("Role", back_populates="user_roles")


# --- SKILLS ---
class Skills(Base):
    __tablename__ = "skills"

    skill_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    skill_name = Column(String, unique=True, nullable=False)
    category = Column(String, nullable=False)  # technical, soft, domain-specific
    description = Column(Text)
    industry_relevance = Column(JSON, default=[])  # Industries where this skill is valuable
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    user_skills = relationship("UserSkills", back_populates="skill", cascade="all, delete-orphan")
    learning_resources = relationship("LearningResources", back_populates="skill", cascade="all, delete-orphan")


class UserSkills(Base):
    __tablename__ = "user_skills"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # association PK
    user_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.skill_id", ondelete="CASCADE"), nullable=False)

    skill_name = Column(String, nullable=False)  # redundant, but okay if you want denormalized lookup
    proficiency_level = Column(String)  # beginner, intermediate, advanced, expert
    years_of_experience = Column(Integer, default=0)
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)

    # Unique constraint to prevent duplicate entries
    __table_args__ = (UniqueConstraint("user_id", "skill_id", name="unique_user_skill"),)

    # Relationships
    user = relationship("User", back_populates="skills")
    skill = relationship("Skills", back_populates="user_skills")
    assessments = relationship("Assessment", back_populates="user_skill")

# --- LEARNING RESOURCES ---
class LearningResources(Base):
    __tablename__ = "learning_resources"

    resource_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.skill_id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    url = Column(String, nullable=False)
    resource_type = Column(Enum("article", "video", "course", "book", "tutorial", "practice", name="resource_type"), nullable=False)
    difficulty_level = Column(Enum("beginner", "intermediate", "advanced", "expert", name="difficulty_level"), nullable=False)
    estimated_duration = Column(Integer)  # in minutes
    rating = Column(Float)
    cost_type = Column(Enum("free", "paid", "subscription", name="cost_type"), default="free")
    tags = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    skill = relationship("Skills", back_populates="learning_resources")

# --- PSYCHOMETRIC TESTS (Enhanced for Gamification) ---
class PsychometricTest(Base):
    __tablename__ = "psychometric_tests"

    test_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    test_type = Column(Enum("MBTI", "DISC", "Big Five", "Career Interest", "Learning Style", name="test_type"), nullable=False)
    results = Column(JSON, nullable=False)
    personality_traits = Column(JSON, default={})
    career_preferences = Column(JSON, default={})
    learning_preferences = Column(JSON, default={})
    completion_score = Column(Float, default=0.0)  # Gamification score
    time_taken = Column(Integer)  # in minutes
    taken_at = Column(DateTime, default=datetime.now, index=True)
    is_complete = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    user = relationship("User", back_populates="psychometric_tests")

# --- CAREER PATHS AND RECOMMENDATIONS ---
class CareerPath(Base):
    __tablename__ = "career_paths"
    
    path_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text)
    industry = Column(String, nullable=False)
    required_skills = Column(JSON, default=[])  # List of skill IDs
    preferred_personality_traits = Column(JSON, default={})
    salary_range = Column(JSON, default={})  # min, max, currency
    growth_prospects = Column(String)
    education_requirements = Column(JSON, default=[])
    experience_requirements = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    career_recommendations = relationship("CareerRecommendation", back_populates="career_path")

class CareerRecommendation(Base):
    __tablename__ = "career_recommendations"
    
    recommendation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    career_path_id = Column(UUID(as_uuid=True), ForeignKey("career_paths.path_id"), nullable=False)
    match_score = Column(Float, nullable=False)  # 0.0 to 1.0
    reasoning = Column(Text)  # AI-generated explanation
    skill_gap_analysis = Column(JSON, default={})
    recommended_actions = Column(JSON, default=[])
    priority_level = Column(Enum("high", "medium", "low", name="priority_level"), default="medium")
    is_viewed = Column(Boolean, default=False)
    is_bookmarked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    user = relationship("User", back_populates="career_recommendations")
    career_path = relationship("CareerPath", back_populates="career_recommendations")

# --- ROADMAPS (Enhanced) ---
class Roadmap(Base):
    __tablename__ = "roadmaps"
    
    roadmap_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    career_path = Column(String)
    progress_percentage = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    user = relationship("User", back_populates="roadmaps")
    milestones = relationship("Milestone", back_populates="roadmap", cascade="all, delete-orphan")


class Milestone(Base):
    __tablename__ = "milestones"
    
    milestone_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    roadmap_id = Column(UUID(as_uuid=True), ForeignKey("roadmaps.roadmap_id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    order_sequence = Column(Integer, nullable=False)
    estimated_duration = Column(Integer)  # in weeks
    required_skills = Column(JSON, default=[])
    learning_resources = Column(JSON, default=[])
    success_criteria = Column(Text)
    status = Column(Enum("not_started", "in_progress", "completed", "skipped", name="milestone_status"), default="not_started")
    completion_date = Column(DateTime, nullable=True)
    points_awarded = Column(Integer, default=0)  # Gamification
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationship back to Roadmap
    roadmap = relationship("Roadmap", back_populates="milestones")

# --- ASSESSMENTS ---
class Assessment(Base):
    __tablename__ = "assessments"

    assessment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    user_skill_id = Column(UUID(as_uuid=True), ForeignKey("user_skills.id", ondelete="CASCADE"))
    assessment_type = Column(Enum("skill_test", "practice_quiz", "certification", name="assessment_type"), default="skill_test")
    score = Column(Integer, nullable=False)
    max_score = Column(Integer, nullable=False)
    percentage = Column(Float, nullable=False)
    time_taken = Column(Integer)  # in minutes
    attempts_count = Column(Integer, default=1)
    is_passed = Column(Boolean, default=False)
    points_earned = Column(Integer, default=0)  # Gamification
    taken_at = Column(DateTime, default=datetime.now, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    user = relationship("User", back_populates="assessments")
    user_skill = relationship("UserSkills", back_populates="assessments")
    questions = relationship("AssessmentQuestion", back_populates="assessment", cascade="all, delete-orphan")

class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"

    question_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("assessments.assessment_id"), nullable=False, index=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(Enum("multiple_choice", "true_false", "short_answer", "coding", name="question_type"), default="multiple_choice")
    options = Column(JSON, default=[])  # For multiple choice questions
    correct_answer = Column(Text, nullable=False)
    user_answer = Column(Text)
    points = Column(Integer, nullable=False)
    is_correct = Column(Boolean, default=False)
    time_taken = Column(Integer)  # in seconds
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    assessment = relationship("Assessment", back_populates="questions")

# # --- MENTORSHIP ---
# class MentorshipSession(Base):
    # __tablename__ = "mentorship_sessions"

    # session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # mentor_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    # mentee_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    # session_type = Column(Enum("career_guidance", "skill_development", "interview_prep", "general", name="session_type"), default="general")
    # scheduled_time = Column(DateTime, nullable=False, index=True)
    # duration_minutes = Column(Integer, nullable=False)
    # actual_duration = Column(Integer, nullable=True)
    # status = Column(Enum("scheduled", "in_progress", "completed", "canceled", "no_show", name="session_status"), default="scheduled")
    # meeting_url = Column(String)
    # agenda = Column(Text)
    # notes = Column(Text)
    # mentor_feedback = Column(Text)
    # mentee_feedback = Column(Text)
    # rating = Column(Integer)  # 1-5 stars
    # points_earned = Column(Integer, default=0)  # Gamification for mentee
    # created_at = Column(DateTime, default=datetime.now)
    # updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # # Relationships
    # mentor = relationship("User", foreign_keys=[mentor_id], back_populates="mentorship_as_mentor")
    # mentee = relationship("User", foreign_keys=[mentee_id], back_populates="mentorship_as_mentee")

# --- GAMIFICATION SYSTEM ---
class GamificationProfile(Base):
    __tablename__ = "gamification_profiles"
    
    profile_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, unique=True)
    total_points = Column(Integer, default=0)
    current_level = Column(Integer, default=1)
    experience_points = Column(Integer, default=0)
    badges_earned = Column(JSON, default=[])
    achievements_unlocked = Column(JSON, default=[])
    streak_days = Column(Integer, default=0)
    last_activity_date = Column(Date, default=date.today)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    user = relationship("User", back_populates="gamification_profile")

class Badge(Base):
    __tablename__ = "badges"
    
    badge_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    icon_url = Column(String)
    category = Column(Enum("skill", "assessment", "mentorship", "completion", "streak", name="badge_category"))
    points_required = Column(Integer, default=0)
    criteria = Column(JSON, default={})
    rarity = Column(Enum("common", "uncommon", "rare", "epic", "legendary", name="badge_rarity"), default="common")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class UserBadge(Base):
    __tablename__ = "user_badges"
    
    user_badge_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    badge_id = Column(UUID(as_uuid=True), ForeignKey("badges.badge_id"), nullable=False)
    earned_at = Column(DateTime, default=datetime.now)
    
    # Unique constraint
    __table_args__ = (UniqueConstraint('user_id', 'badge_id', name='unique_user_badge'),)
    
    # Relationships
    user = relationship("User")
    badge = relationship("Badge")

# --- AI AGENT INTERACTIONS ---
class AgentInteraction(Base):
    __tablename__ = "agent_interactions"
    
    interaction_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    agent_type = Column(Enum("career_counselor", "skill_assessor", "mentor_matcher", "roadmap_generator", name="agent_type"))
    interaction_type = Column(Enum("chat", "recommendation", "assessment", "guidance", name="interaction_type"))
    user_message = Column(Text)
    agent_response = Column(Text)
    context_data = Column(JSON, default={})
    satisfaction_rating = Column(Integer)  # 1-5 stars
    session_token = Column(String)
    created_at = Column(DateTime, default=datetime.now, index=True)
    
    # Relationships
    user = relationship("User")

# Create indexes for better performance
Index('idx_user_skills_user_id', UserSkills.user_id)
Index('idx_user_skills_skill_id', UserSkills.skill_id)
Index('idx_assessments_user_skill', Assessment.user_skill_id)
Index('idx_roadmaps_user_id', Roadmap.user_id)
# Index('idx_mentorship_mentor', MentorshipSession.mentor_id)
# Index('idx_mentorship_mentee', MentorshipSession.mentee_id)
Index('idx_agent_interactions_user', AgentInteraction.user_id)
Index('idx_career_recommendations_user', CareerRecommendation.user_id)