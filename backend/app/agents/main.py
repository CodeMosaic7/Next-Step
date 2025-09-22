import asyncio
from typing import Optional
import uuid

from .Councellor_agent import CounsellorAgent
from .Coordinator_agent import CoordinatorAgent,CoordinatorState
from .Psychologist_agent import PsychologistAgent
from app.pydantic_schema.Enums import AssessmentType,ConsultationStatus

class CoordinatorSystem:
    """Main system that orchestrates the entire consultation process"""
    
    def __init__(self):
        self.coordinator = CoordinatorAgent()
        self.psychologist = PsychologistAgent()
        self.counsellor = CounsellorAgent()
        self.active_consultations = {}
    
    async def process_assessment_report(self, user_id: str, assessment_report: str, assessment_type: AssessmentType) -> str:
        """Main entry point: process assessment report and return comprehensive analysis"""
        
        session_id = str(uuid.uuid4())
        
        # Initialize state
        state = CoordinatorState(
            user_id=user_id,
            session_id=session_id,
            assessment_report=assessment_report,
            assessment_type=assessment_type
        )
        
        try:
            # Step 1: Analyze support needs
            print("Step 1: Analyzing support needs...")
            support_needs = await self.coordinator.analyze_support_needs(assessment_report)
            
            state.needs_mental_health_support = support_needs.get("needs_mental_health", True)
            state.needs_career_guidance = support_needs.get("needs_career_guidance", True)
            
            # Step 2: Consult specialists in parallel
            print("Step 2: Consulting specialists...")
            tasks = []
            
            if state.needs_mental_health_support:
                tasks.append(self.psychologist.analyze_report(assessment_report, assessment_type))
            else:
                tasks.append(asyncio.create_task(self._return_none()))
            
            if state.needs_career_guidance:
                tasks.append(self.counsellor.provide_guidance(assessment_report, assessment_type))
            else:
                tasks.append(asyncio.create_task(self._return_none()))
            
            # Wait for both analyses to complete
            psychological_analysis, career_guidance = await asyncio.gather(*tasks)
            
            state.psychologist_analysis = psychological_analysis
            state.counsellor_guidance = career_guidance
            
            # Step 3: Synthesize final report
            print("Step 3: Synthesizing final report...")
            comprehensive_report = await self.coordinator.synthesize_reports(
                psychological_analysis or "No psychological analysis needed",
                career_guidance or "No career guidance needed", 
                assessment_type
            )
            
            state.comprehensive_report = comprehensive_report
            state.consultation_status = ConsultationStatus.COMPLETED
            
            # Store session
            self.active_consultations[session_id] = state
            
            return comprehensive_report
            
        except Exception as e:
            error_message = f"Error processing assessment: {str(e)}"
            print(error_message)
            return error_message
    
    async def _return_none(self):
        """Helper function for conditional parallel processing"""
        return None
    
    def get_consultation_status(self, session_id: str) -> Optional[ConsultationStatus]:
        """Get status of a consultation session"""
        if session_id in self.active_consultations:
            return self.active_consultations[session_id].consultation_status
        return None
    
    def get_psychological_analysis(self, session_id: str) -> Optional[str]:
        """Get just the psychological analysis"""
        if session_id in self.active_consultations:
            return self.active_consultations[session_id].psychologist_analysis
        return None
    
    def get_career_guidance(self, session_id: str) -> Optional[str]:
        """Get just the career guidance"""
        if session_id in self.active_consultations:
            return self.active_consultations[session_id].counsellor_guidance
        return None

# ============================================================================
# USAGE EXAMPLE
# ============================================================================

async def main():
    """Example usage of the coordinator system"""
    
    # Sample assessment report (this would come from your AssessmentBot)
    sample_report = """
    [Question: When working on a challenging project, what is your preferred approach?
    Answer given by user: A) Work alone and focus deeply
    What it means: This indicates a preference for independent work and deep focus, suggesting introverted tendencies and strong concentration abilities.]
    
    [Question: How do you typically handle stress?
    Answer given by user: 4 - Agree (I handle stress well)
    What it means: Shows good stress management skills and emotional resilience, indicating strong coping mechanisms.]
    
    [Question: What motivates you most in your career?
    Answer given by user: D) Use a combination of logic and intuition
    What it means: Demonstrates balanced decision-making approach, combining analytical thinking with emotional intelligence.]
    
    SUMMARY:
    - Overall personality profile: Independent, analytical thinker with good stress management
    - Key strengths identified: Deep focus, emotional resilience, balanced decision-making
    - Areas for development: May benefit from more collaborative experiences
    - Career recommendations: Roles requiring independent analysis, research, or specialized expertise
    """
    
    # Initialize coordinator system
    coordinator_system = CoordinatorSystem()
    
    # Process the assessment report
    print("Processing assessment report...")
    print("=" * 60)
    
    user_id = "user_123"
    comprehensive_report = await coordinator_system.process_assessment_report(
        user_id=user_id,
        assessment_report=sample_report,
        assessment_type=AssessmentType.PSYCHOMETRIC
    )
    
    print("COMPREHENSIVE CONSULTATION REPORT:")
    print("=" * 60)
    print(comprehensive_report)

if __name__ == "__main__":
    asyncio.run(main())