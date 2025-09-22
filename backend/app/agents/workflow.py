from langchain.schema import AIMessage
from typing import List

from .Coordinator_agent import CoordinatorAgent, CoordinatorState
from .Councellor_agent import CounsellorAgent
from .Psychologist_agent import PsychologistAgent
from app.pydantic_schema.Enums import SupportType, ConsultationStatus

async def receive_assessment_report(state: CoordinatorState) -> CoordinatorState:
    """Initial step: receive and log the assessment report"""
    print(f"Coordinator received assessment report for user {state.user_id}")
    
    state.messages.append(
        AIMessage(content="Assessment report received. Analyzing support needs...")
    )
    state.current_step = "analyzing_needs"
    
    return state

async def analyze_support_needs(state: CoordinatorState) -> CoordinatorState:
    """Analyze what type of support the user needs"""
    print("Analyzing support needs...")
    
    coordinator = CoordinatorAgent()
    support_needs = await coordinator.analyze_support_needs(state.assessment_report)
    
    state.needs_mental_health_support = support_needs.get("needs_mental_health", True)
    state.needs_career_guidance = support_needs.get("needs_career_guidance", True)
    
    priority = support_needs.get("priority", "both")
    if priority == "mental_health":
        state.support_priority = SupportType.MENTAL_HEALTH
    elif priority == "career_guidance":
        state.support_priority = SupportType.CAREER_GUIDANCE
    else:
        state.support_priority = SupportType.BOTH
    
    state.current_step = "routing_to_specialists"
    state.consultation_status = ConsultationStatus.IN_PROGRESS
    
    return state

async def consult_psychologist(state: CoordinatorState) -> CoordinatorState:
    """Route to psychologist for mental health analysis"""
    print("Consulting psychologist...")
    
    psychologist = PsychologistAgent()
    analysis = await psychologist.analyze_report(
        state.assessment_report, 
        state.assessment_type
    )
    
    state.psychologist_analysis = analysis
    state.messages.append(
        AIMessage(content="Psychological analysis completed.")
    )
    
    return state

async def consult_counsellor(state: CoordinatorState) -> CoordinatorState:
    """Route to counsellor for career guidance"""
    print("Consulting career counsellor...")
    
    counsellor = CounsellorAgent()
    guidance = await counsellor.provide_guidance(
        state.assessment_report,
        state.assessment_type
    )
    
    state.counsellor_guidance = guidance
    state.messages.append(
        AIMessage(content="Career guidance analysis completed.")
    )
    
    return state

async def synthesize_final_report(state: CoordinatorState) -> CoordinatorState:
    """Combine all analyses into final comprehensive report"""
    print("Synthesizing final report...")
    
    coordinator = CoordinatorAgent()
    
    # Ensure we have both analyses
    psychological_analysis = state.psychologist_analysis or "No psychological analysis available"
    career_guidance = state.counsellor_guidance or "No career guidance available"
    
    comprehensive_report = await coordinator.synthesize_reports(
        psychological_analysis,
        career_guidance,
        state.assessment_type
    )
    
    state.comprehensive_report = comprehensive_report
    state.consultation_status = ConsultationStatus.COMPLETED
    state.current_step = "completed"
    
    state.messages.append(
        AIMessage(content="Comprehensive consultation report ready!")
    )
    
    return state

def should_consult_psychologist(state: CoordinatorState) -> bool:
    """Check if psychological consultation is needed"""
    return state.needs_mental_health_support

def should_consult_counsellor(state: CoordinatorState) -> bool:
    """Check if career counselling is needed"""
    return state.needs_career_guidance

def routing_decision(state: CoordinatorState) -> List[str]:
    """Determine which specialists to consult"""
    routes = []
    
    if state.needs_mental_health_support:
        routes.append("consult_psychologist")
    
    if state.needs_career_guidance:
        routes.append("consult_counsellor")
    
    return routes or ["synthesize_final_report"]
