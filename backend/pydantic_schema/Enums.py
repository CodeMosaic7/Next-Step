from enum import Enum
class RoleNameEnum(str, Enum):
    ADMIN = "admin"
    MENTORS = "mentors"
    STUDENT = "student"
    CAREER_COUNSELOR = "career_counselor"

class ProficiencyLevelEnum(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class ResourceTypeEnum(str, Enum):
    ARTICLE = "article"
    VIDEO = "video"
    COURSE = "course"
    BOOK = "book"
    TUTORIAL = "tutorial"
    PRACTICE = "practice"

class CostTypeEnum(str, Enum):
    FREE = "free"
    PAID = "paid"
    SUBSCRIPTION = "subscription"

class TestTypeEnum(str, Enum):
    MBTI = "MBTI"
    DISC = "DISC"
    BIG_FIVE = "Big Five"
    CAREER_INTEREST = "Career Interest"
    LEARNING_STYLE = "Learning Style"

class PriorityLevelEnum(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class RoadmapStatusEnum(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"

class MilestoneStatusEnum(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class QuestionTypeEnum(str, Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    CODING = "coding"

class SessionTypeEnum(str, Enum):
    CAREER_GUIDANCE = "career_guidance"
    SKILL_DEVELOPMENT = "skill_development"
    INTERVIEW_PREP = "interview_prep"
    GENERAL = "general"

class SessionStatusEnum(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELED = "canceled"
    NO_SHOW = "no_show"

class BadgeCategoryEnum(str, Enum):
    SKILL = "skill"
    ASSESSMENT = "assessment"
    MENTORSHIP = "mentorship"
    COMPLETION = "completion"
    STREAK = "streak"

class BadgeRarityEnum(str, Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"

class AgentTypeEnum(str, Enum):
    CAREER_COUNSELOR = "career_counselor"
    SKILL_ASSESSOR = "skill_assessor"
    MENTOR_MATCHER = "mentor_matcher"
    ROADMAP_GENERATOR = "roadmap_generator"

class InteractionTypeEnum(str, Enum):
    CHAT = "chat"
    RECOMMENDATION = "recommendation"
    ASSESSMENT = "assessment"
    GUIDANCE = "guidance"


class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    LIKERT_SCALE = "likert_scale"
    TRUE_FALSE = "true_false"
    OPEN_ENDED = "open_ended"

class AssessmentType(str, Enum):
    PSYCHOMETRIC = "psychometric"
    APTITUDE = "aptitude"
    PERSONALITY = "personality"

class SupportType(Enum):
    MENTAL_HEALTH = "mental_health"
    CAREER_GUIDANCE = "career_guidance"
    BOTH = "both"

class ConsultationStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
