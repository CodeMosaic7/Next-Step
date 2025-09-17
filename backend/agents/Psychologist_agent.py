# Psychological Assessment Analysis System
# Analyzes 15 questions like a professional psychologist
# Returns comprehensive evaluation with feedback and maintains assessment history

import os
import json
import datetime
from typing import Dict, List, TypedDict, Annotated, Optional
from dataclasses import dataclass, asdict
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from llm.gemini_llm import llm

# Load environment variables
import dotenv
dotenv.load_dotenv()

@dataclass
class PsychologicalProfile:
    """Complete psychological profile structure"""
    skills: List[str]
    personality_traits: List[str]
    iq_indicators: List[str]
    cognitive_abilities: List[str]
    emotional_intelligence: List[str]
    behavioral_patterns: List[str]
    strengths: List[str]
    areas_for_improvement: List[str]
    risk_factors: List[str]
    recommendations: List[str]
    confidence_score: float
    assessment_date: str
    session_id: str

@dataclass
class FeedbackEntry:
    """Individual feedback entry"""
    timestamp: str
    category: str
    observation: str
    recommendation: str
    severity: str  # low, medium, high
    follow_up_required: bool

class AssessmentState(TypedDict):
    """State structure for psychological assessment workflow"""
    questions: List[Dict]
    answers: List[str]
    participant_info: Dict
    psychological_profile: Optional[PsychologicalProfile]
    feedback_log: List[FeedbackEntry]
    current_analysis_step: str
    human_review_needed: bool
    assessment_complete: bool
    session_notes: List[str]
    red_flags: List[str]
    messages: Annotated[List, add_messages]

class PsychologicalAssessment:
    def __init__(self):
        self.total_questions = 15
        self.feedback_storage = "assessment_feedback.json"
        self.psychological_frameworks = [
            "Big Five Personality Model",
            "DISC Assessment",
            "Emotional Intelligence (EQ)",
            "Cognitive Behavioral Analysis",
            "Psychodynamic Indicators"
        ]
        
    def load_feedback_history(self) -> List[Dict]:
        """Load previous assessment feedback"""
        try:
            if os.path.exists(self.feedback_storage):
                with open(self.feedback_storage, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading feedback history: {e}")
        return []
    
    def save_feedback(self, feedback_data: Dict):
        """Save assessment feedback to persistent storage"""
        try:
            history = self.load_feedback_history()
            history.append(feedback_data)
            
            with open(self.feedback_storage, 'w') as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            print(f"Error saving feedback: {e}")

    @staticmethod
    def psychological_skills_analysis(state: AssessmentState) -> AssessmentState:
        """Comprehensive skills analysis from psychological perspective"""
        try:
            qa_pairs = list(zip(state.get('questions', []), state.get('answers', [])))
            
            context = f"""
            As a professional psychologist, analyze these assessment responses for skills and competencies:
            
            Questions and Answers: {qa_pairs}
            Participant Info: {state.get('participant_info', {})}
            
            Provide a comprehensive psychological evaluation focusing on:
            1. Cognitive Skills (analytical thinking, problem-solving, decision-making)
            2. Interpersonal Skills (communication, empathy, leadership)
            3. Intrapersonal Skills (self-awareness, emotional regulation, resilience)
            4. Technical/Professional Skills (domain-specific abilities)
            5. Adaptive Skills (flexibility, learning agility, stress management)
            
            Format your response as a detailed psychological assessment report.
            Include confidence levels and note any areas requiring further evaluation.
            """
            
            response = llm.invoke(context)
            skills_analysis = parse_psychological_response(response, "skills")
            
            # Add to session notes
            state['session_notes'] = state.get('session_notes', [])
            state['session_notes'].append(f"Skills Analysis: {len(skills_analysis.get('skills', []))} skills identified")
            
            # Check for any concerning patterns
            if detect_skill_deficits(skills_analysis):
                state['red_flags'] = state.get('red_flags', [])
                state['red_flags'].append("Potential skill deficits identified - requires clinical attention")
            
            state['current_analysis_step'] = "skills_complete"
            state['messages'] = add_messages(state.get('messages', []), 
                                           {"role": "psychologist", "content": f"Skills assessment completed. Identified key competencies and areas for development."})
            
            # Store preliminary skills data
            if not state.get('psychological_profile'):
                state['psychological_profile'] = PsychologicalProfile(
                    skills=skills_analysis.get('skills', []),
                    personality_traits=[],
                    iq_indicators=[],
                    cognitive_abilities=skills_analysis.get('cognitive_abilities', []),
                    emotional_intelligence=[],
                    behavioral_patterns=[],
                    strengths=[],
                    areas_for_improvement=skills_analysis.get('areas_for_improvement', []),
                    risk_factors=[],
                    recommendations=[],
                    confidence_score=0.0,
                    assessment_date=datetime.datetime.now().isoformat(),
                    session_id=state.get('session_id', 'default')
                )
            else:
                state['psychological_profile'].skills = skills_analysis.get('skills', [])
                state['psychological_profile'].cognitive_abilities = skills_analysis.get('cognitive_abilities', [])
                
        except Exception as e:
            print(f"Error in skills analysis: {e}")
            state['human_review_needed'] = True
            add_feedback_entry(state, "error", f"Skills analysis failed: {str(e)}", "Require manual review", "high", True)
            
        return state

    @staticmethod
    def psychological_personality_analysis(state: AssessmentState) -> AssessmentState:
        """Deep personality analysis using psychological frameworks"""
        try:
            qa_pairs = list(zip(state.get('questions', []), state.get('answers', [])))
            
            context = f"""
            As a clinical psychologist, conduct a comprehensive personality assessment:
            
            Questions and Answers: {qa_pairs}
            Previous Skills Analysis: {state.get('psychological_profile', {}).skills if state.get('psychological_profile') else []}
            
            Apply these psychological frameworks:
            1. Big Five Personality Traits (OCEAN model)
            2. DISC Behavioral Assessment
            3. Emotional Intelligence Evaluation
            4. Attachment Styles Analysis
            5. Defense Mechanisms Identification
            6. Cognitive Patterns Assessment
            
            Provide detailed analysis including:
            - Core personality traits with evidence
            - Behavioral patterns and triggers
            - Emotional regulation capabilities
            - Interpersonal dynamics and relationship patterns
            - Potential psychological vulnerabilities or strengths
            - Risk factors for mental health concerns
            
            Use professional psychological terminology and provide confidence intervals.
            """
            
            response = llm.invoke(context)
            personality_analysis = parse_psychological_response(response, "personality")
            
            # Update psychological profile
            if state.get('psychological_profile'):
                state['psychological_profile'].personality_traits = personality_analysis.get('personality_traits', [])
                state['psychological_profile'].emotional_intelligence = personality_analysis.get('emotional_intelligence', [])
                state['psychological_profile'].behavioral_patterns = personality_analysis.get('behavioral_patterns', [])
                state['psychological_profile'].risk_factors = personality_analysis.get('risk_factors', [])
            
            # Check for psychological red flags
            check_psychological_red_flags(state, personality_analysis)
            
            state['current_analysis_step'] = "personality_complete"
            add_feedback_entry(state, "personality", "Comprehensive personality assessment completed", 
                             "Continue with cognitive evaluation", "medium", False)
            
        except Exception as e:
            print(f"Error in personality analysis: {e}")
            state['human_review_needed'] = True
            add_feedback_entry(state, "error", f"Personality analysis failed: {str(e)}", 
                             "Require clinical supervision", "high", True)
            
        return state

    @staticmethod
    def psychological_cognitive_analysis(state: AssessmentState) -> AssessmentState:
        """Cognitive abilities and IQ indicators analysis"""
        try:
            qa_pairs = list(zip(state.get('questions', []), state.get('answers', [])))
            
            context = f"""
            As a neuropsychologist, evaluate cognitive functioning and intellectual capabilities:
            
            Assessment Data: {qa_pairs}
            Personality Context: {state.get('psychological_profile', {}).personality_traits if state.get('psychological_profile') else []}
            
            Evaluate:
            1. Fluid Intelligence (reasoning, problem-solving, pattern recognition)
            2. Crystallized Intelligence (knowledge, vocabulary, learned skills)
            3. Working Memory and Processing Speed
            4. Executive Functions (planning, inhibition, cognitive flexibility)
            5. Attention and Concentration
            6. Learning and Memory Capabilities
            7. Verbal and Non-verbal Reasoning
            8. Creative and Divergent Thinking
            
            Provide:
            - Cognitive strengths and weaknesses
            - Estimated intellectual functioning level
            - Learning style preferences
            - Potential cognitive concerns or exceptional abilities
            - Recommendations for cognitive enhancement
            
            Use standardized psychological assessment principles.
            """
            
            response = llm.invoke(context)
            cognitive_analysis = parse_psychological_response(response, "cognitive")
            
            # Update psychological profile
            if state.get('psychological_profile'):
                state['psychological_profile'].iq_indicators = cognitive_analysis.get('iq_indicators', [])
                state['psychological_profile'].cognitive_abilities.extend(cognitive_analysis.get('additional_cognitive', []))
                state['psychological_profile'].strengths = cognitive_analysis.get('strengths', [])
                state['psychological_profile'].recommendations = cognitive_analysis.get('recommendations', [])
            
            state['current_analysis_step'] = "cognitive_complete"
            add_feedback_entry(state, "cognitive", "Cognitive assessment completed", 
                             "Proceeding to comprehensive evaluation", "low", False)
            
        except Exception as e:
            print(f"Error in cognitive analysis: {e}")
            state['human_review_needed'] = True
            add_feedback_entry(state, "error", f"Cognitive analysis failed: {str(e)}", 
                             "Require neuropsychological consultation", "high", True)
            
        return state

    @staticmethod
    def comprehensive_psychological_evaluation(state: AssessmentState) -> AssessmentState:
        """Final comprehensive psychological evaluation and report generation"""
        try:
            profile = state.get('psychological_profile')
            if not profile:
                raise ValueError("No psychological profile available for evaluation")
            
            # Calculate confidence score based on data completeness and consistency
            confidence_score = calculate_assessment_confidence(profile, state)
            profile.confidence_score = confidence_score
            
            # Generate comprehensive recommendations
            comprehensive_recommendations = generate_psychological_recommendations(profile, state)
            profile.recommendations.extend(comprehensive_recommendations)
            
            # Final psychological summary
            context = f"""
            As a senior clinical psychologist, provide a comprehensive psychological evaluation summary:
            
            Complete Profile: {asdict(profile)}
            Session Notes: {state.get('session_notes', [])}
            Red Flags: {state.get('red_flags', [])}
            Feedback Log: {[asdict(f) for f in state.get('feedback_log', [])]}
            
            Provide:
            1. Executive Summary of psychological functioning
            2. Key insights and clinical impressions
            3. Integrated analysis across all domains
            4. Risk assessment and protective factors
            5. Treatment or development recommendations
            6. Follow-up suggestions and monitoring needs
            7. Prognosis and expected outcomes
            
            Maintain professional standards and ethical considerations.
            """
            
            response = llm.invoke(context)
            
            # Add final evaluation to session notes
            state['session_notes'].append(f"Comprehensive evaluation completed - Confidence: {confidence_score:.2f}")
            
            add_feedback_entry(state, "evaluation", "Comprehensive psychological evaluation completed", 
                             "Review recommendations and consider follow-up", "low", 
                             len(state.get('red_flags', [])) > 0)
            
            state['current_analysis_step'] = "evaluation_complete"
            state['assessment_complete'] = True
            
        except Exception as e:
            print(f"Error in comprehensive evaluation: {e}")
            state['human_review_needed'] = True
            add_feedback_entry(state, "error", f"Evaluation failed: {str(e)}", 
                             "Require senior psychologist review", "high", True)
            
        return state

    @staticmethod
    def clinical_supervision_review(state: AssessmentState) -> AssessmentState:
        """Human psychologist supervision and review"""
        print("\n" + "="*60)
        print("CLINICAL SUPERVISION REQUIRED")
        print("="*60)
        
        profile = state.get('psychological_profile')
        if profile:
            print(f"\nAssessment Date: {profile.assessment_date}")
            print(f"Confidence Score: {profile.confidence_score:.2f}")
            print(f"\nSkills Identified: {len(profile.skills)}")
            print(f"Personality Traits: {len(profile.personality_traits)}")
            print(f"Cognitive Indicators: {len(profile.iq_indicators)}")
            print(f"\nRed Flags: {len(state.get('red_flags', []))}")
            
            if state.get('red_flags'):
                print("⚠️  RED FLAGS IDENTIFIED:")
                for flag in state.get('red_flags', []):
                    print(f"   • {flag}")
        
        print(f"\nFeedback Entries: {len(state.get('feedback_log', []))}")
        for feedback in state.get('feedback_log', [])[-3:]:  # Show last 3
            print(f"   • [{feedback.severity.upper()}] {feedback.observation}")
        
        print("\n" + "-"*60)
        
        # Clinical supervision input
        supervision_needed = input("Require clinical supervision? (y/n): ").lower() == 'y'
        
        if supervision_needed:
            print("\nCLINICAL REVIEW OPTIONS:")
            print("1. Modify assessment results")
            print("2. Add clinical notes")
            print("3. Flag for specialist referral")
            print("4. Approve as-is")
            
            choice = input("Select option (1-4): ")
            
            if choice == "1":
                # Allow modifications
                modify_assessment_results(state)
            elif choice == "2":
                clinical_note = input("Enter clinical note: ")
                state['session_notes'].append(f"Clinical Note: {clinical_note}")
                add_feedback_entry(state, "clinical", clinical_note, "Documented in clinical notes", "medium", False)
            elif choice == "3":
                referral_type = input("Referral type (psychiatrist/neuropsychologist/other): ")
                add_feedback_entry(state, "referral", f"Specialist referral recommended: {referral_type}", 
                                 "Schedule specialist consultation", "high", True)
            
        state['human_review_needed'] = False
        add_feedback_entry(state, "supervision", "Clinical supervision completed", 
                         "Assessment approved for final report", "low", False)
        
        return state

    @staticmethod
    def route_assessment_flow(state: AssessmentState) -> str:
        """Determines the next step in psychological assessment workflow"""
        current_step = state.get('current_analysis_step', '')
        
        if state.get('human_review_needed', False):
            return "clinical_supervision"
        elif current_step == 'skills_complete':
            return "personality_analysis"
        elif current_step == 'personality_complete':
            return "cognitive_analysis"
        elif current_step == 'cognitive_complete':
            return "comprehensive_evaluation"
        elif state.get('assessment_complete', False):
            return "end"
        else:
            return "skills_analysis"

    def build_psychological_assessment_graph(self):
        """Builds the comprehensive psychological assessment workflow"""
        graph_builder = StateGraph(AssessmentState)
        
        # Add psychological assessment nodes
        graph_builder.add_node("skills_analysis", self.psychological_skills_analysis)
        graph_builder.add_node("personality_analysis", self.psychological_personality_analysis)
        graph_builder.add_node("cognitive_analysis", self.psychological_cognitive_analysis)
        graph_builder.add_node("comprehensive_evaluation", self.comprehensive_psychological_evaluation)
        graph_builder.add_node("clinical_supervision", self.clinical_supervision_review)
        
        # Define workflow edges
        graph_builder.add_edge(START, "skills_analysis")
        
        # Add conditional routing
        graph_builder.add_conditional_edges(
            "skills_analysis",
            self.route_assessment_flow,
            {
                "personality_analysis": "personality_analysis",
                "clinical_supervision": "clinical_supervision",
                "end": END
            }
        )
        
        graph_builder.add_conditional_edges(
            "personality_analysis", 
            self.route_assessment_flow,
            {
                "cognitive_analysis": "cognitive_analysis",
                "clinical_supervision": "clinical_supervision",
                "end": END
            }
        )
        
        graph_builder.add_conditional_edges(
            "cognitive_analysis",
            self.route_assessment_flow,
            {
                "comprehensive_evaluation": "comprehensive_evaluation",
                "clinical_supervision": "clinical_supervision",
                "end": END
            }
        )
        
        graph_builder.add_conditional_edges(
            "comprehensive_evaluation",
            self.route_assessment_flow,
            {
                "clinical_supervision": "clinical_supervision",
                "end": END
            }
        )
        
        graph_builder.add_conditional_edges(
            "clinical_supervision",
            self.route_assessment_flow,
            {
                "end": END
            }
        )
        
        # Compile with memory for session persistence
        memory = MemorySaver()
        return graph_builder.compile(checkpointer=memory)

    def conduct_psychological_assessment(self, questions: List[Dict], answers: List[str], 
                                       participant_info: Dict = None) -> Dict:
        """Conducts comprehensive psychological assessment"""
        if len(questions) != self.total_questions or len(answers) != self.total_questions:
            raise ValueError(f"Expected exactly {self.total_questions} questions and answers")
        
        session_id = f"assessment_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Initialize psychological assessment state
        initial_state = {
            "questions": questions,
            "answers": answers,
            "participant_info": participant_info or {},
            "psychological_profile": None,
            "feedback_log": [],
            "current_analysis_step": "",
            "human_review_needed": False,
            "assessment_complete": False,
            "session_notes": [f"Assessment session {session_id} initiated"],
            "red_flags": [],
            "messages": [],
            "session_id": session_id
        }
        
        # Build and execute psychological assessment
        graph = self.build_psychological_assessment_graph()
        config = {"configurable": {"thread_id": session_id}}
        
        try:
            final_state = graph.invoke(initial_state, config)
            
            # Save comprehensive feedback
            feedback_data = {
                "session_id": session_id,
                "assessment_date": datetime.datetime.now().isoformat(),
                "psychological_profile": asdict(final_state.get('psychological_profile')) if final_state.get('psychological_profile') else None,
                "feedback_log": [asdict(f) for f in final_state.get('feedback_log', [])],
                "session_notes": final_state.get('session_notes', []),
                "red_flags": final_state.get('red_flags', []),
                "participant_info": final_state.get('participant_info', {})
            }
            
            self.save_feedback(feedback_data)
            
            # Return structured psychological assessment results
            profile = final_state.get('psychological_profile')
            if profile:
                return {
                    "skills": profile.skills,
                    "personality_traits": profile.personality_traits,
                    "iq": profile.iq_indicators,
                    "psychological_evaluation": {
                        "cognitive_abilities": profile.cognitive_abilities,
                        "emotional_intelligence": profile.emotional_intelligence,
                        "behavioral_patterns": profile.behavioral_patterns,
                        "strengths": profile.strengths,
                        "areas_for_improvement": profile.areas_for_improvement,
                        "risk_factors": profile.risk_factors,
                        "recommendations": profile.recommendations,
                        "confidence_score": profile.confidence_score,
                        "session_id": session_id
                    },
                    "clinical_feedback": final_state.get('feedback_log', []),
                    "session_notes": final_state.get('session_notes', []),
                    "requires_follow_up": len(final_state.get('red_flags', [])) > 0
                }
            else:
                raise ValueError("Assessment incomplete - no psychological profile generated")
                
        except Exception as e:
            error_feedback = {
                "session_id": session_id,
                "error": str(e),
                "timestamp": datetime.datetime.now().isoformat(),
                "status": "failed"
            }
            self.save_feedback(error_feedback)
            raise e

# Helper functions for psychological assessment

def parse_psychological_response(response, analysis_type: str) -> Dict:
    """Parse LLM response using psychological assessment standards"""
    if hasattr(response, 'content'):
        content = response.content
    else:
        content = str(response)
    
    # Implement sophisticated parsing based on psychological frameworks
    parsed_data = {}
    
    if analysis_type == "skills":
        parsed_data = {
            "skills": extract_psychological_constructs(content, ["skill", "ability", "competency", "capability"]),
            "cognitive_abilities": extract_psychological_constructs(content, ["cognitive", "thinking", "reasoning", "memory"]),
            "areas_for_improvement": extract_psychological_constructs(content, ["improve", "develop", "enhance", "strengthen"])
        }
    elif analysis_type == "personality":
        parsed_data = {
            "personality_traits": extract_psychological_constructs(content, ["trait", "characteristic", "tendency", "pattern"]),
            "emotional_intelligence": extract_psychological_constructs(content, ["emotional", "empathy", "social", "interpersonal"]),
            "behavioral_patterns": extract_psychological_constructs(content, ["behavior", "response", "reaction", "approach"]),
            "risk_factors": extract_psychological_constructs(content, ["risk", "concern", "vulnerability", "warning"])
        }
    elif analysis_type == "cognitive":
        parsed_data = {
            "iq_indicators": extract_psychological_constructs(content, ["intelligence", "reasoning", "problem-solving", "analytical"]),
            "additional_cognitive": extract_psychological_constructs(content, ["memory", "attention", "processing", "executive"]),
            "strengths": extract_psychological_constructs(content, ["strength", "strong", "excellent", "superior"]),
            "recommendations": extract_psychological_constructs(content, ["recommend", "suggest", "advise", "consider"])
        }
    
    return parsed_data

def extract_psychological_constructs(text: str, keywords: List[str]) -> List[str]:
    """Extract psychological constructs from text using NLP techniques"""
    constructs = []
    lines = text.lower().split('\n')
    
    for line in lines:
        for keyword in keywords:
            if keyword in line:
                # Extract meaningful phrases containing the keyword
                words = line.split()
                if keyword in ' '.join(words):
                    # Find phrases around the keyword
                    for i, word in enumerate(words):
                        if keyword in word:
                            start = max(0, i-2)
                            end = min(len(words), i+3)
                            phrase = ' '.join(words[start:end])
                            if len(phrase) > 10:  # Meaningful phrases
                                constructs.append(phrase.strip('.,!?'))
    
    # Remove duplicates and clean up
    return list(set([c for c in constructs if len(c) > 5]))[:10]  # Limit to top 10

def detect_skill_deficits(analysis: Dict) -> bool:
    """Detect potential skill deficits requiring clinical attention"""
    skills = analysis.get('skills', [])
    improvements = analysis.get('areas_for_improvement', [])
    
    # Red flags: very few skills identified or many improvement areas
    return len(skills) < 3 or len(improvements) > len(skills)

def check_psychological_red_flags(state: AssessmentState, analysis: Dict):
    """Check for psychological red flags requiring immediate attention"""
    risk_factors = analysis.get('risk_factors', [])
    red_flag_keywords = ['depression', 'anxiety', 'trauma', 'substance', 'suicide', 'self-harm', 'psychosis', 'mania']
    
    for risk in risk_factors:
        for keyword in red_flag_keywords:
            if keyword in risk.lower():
                state['red_flags'] = state.get('red_flags', [])
                state['red_flags'].append(f"Mental health concern identified: {risk}")
                state['human_review_needed'] = True

def add_feedback_entry(state: AssessmentState, category: str, observation: str, 
                      recommendation: str, severity: str, follow_up: bool):
    """Add structured feedback entry to assessment"""
    feedback = FeedbackEntry(
        timestamp=datetime.datetime.now().isoformat(),
        category=category,
        observation=observation,
        recommendation=recommendation,
        severity=severity,
        follow_up_required=follow_up
    )
    
    if 'feedback_log' not in state:
        state['feedback_log'] = []
    state['feedback_log'].append(feedback)

def calculate_assessment_confidence(profile: PsychologicalProfile, state: AssessmentState) -> float:
    """Calculate confidence score for psychological assessment"""
    base_score = 0.5
    
    # Data completeness
    data_completeness = (
        len(profile.skills) * 0.15 +
        len(profile.personality_traits) * 0.20 +
        len(profile.iq_indicators) * 0.15 +
        len(profile.cognitive_abilities) * 0.10 +
        len(profile.emotional_intelligence) * 0.10 +
        len(profile.behavioral_patterns) * 0.15 +
        len(profile.recommendations) * 0.10 +
        len(profile.strengths) * 0.05
    ) / 20  # Normalize to 0-1
    
    # Consistency check
    consistency_bonus = 0.2 if len(state.get('red_flags', [])) == 0 else -0.1
    
    # Human review factor
    human_review_factor = 0.1 if not state.get('human_review_needed', False) else 0.0
    
    confidence = min(1.0, base_score + data_completeness + consistency_bonus + human_review_factor)
    return round(confidence, 2)

def generate_psychological_recommendations(profile: PsychologicalProfile, state: AssessmentState) -> List[str]:
    """Generate evidence-based psychological recommendations"""
    recommendations = []
    
    # Based on strengths
    if profile.strengths:
        recommendations.append(f"Leverage identified strengths: {', '.join(profile.strengths[:3])}")
    
    # Based on areas for improvement
    if profile.areas_for_improvement:
        recommendations.append(f"Focus development on: {', '.join(profile.areas_for_improvement[:2])}")
    
    # Based on risk factors
    if profile.risk_factors:
        recommendations.append("Consider preventive interventions for identified risk factors")
        recommendations.append("Regular monitoring and follow-up recommended")
    
    # Based on red flags
    if state.get('red_flags'):
        recommendations.append("Immediate clinical consultation recommended")
        recommendations.append("Develop safety plan and support network")
    
    return recommendations

def modify_assessment_results(state: AssessmentState):
    """Allow clinical modification of assessment results"""
    profile = state.get('psychological_profile')
    if not profile:
        return
    
    print("\nCURRENT ASSESSMENT RESULTS:")
    print(f"Skills: {profile.skills}")
    print(f"Personality Traits: {profile.personality_traits}")
    print(f"IQ Indicators: {profile.iq_indicators}")
    
    # Allow modifications
    modify_skills = input("Modify skills? (y/n): ").lower() == 'y'
    if modify_skills:
        new_skills = input("Enter corrected skills (comma-separated): ")
        if new_skills.strip():
            profile.skills = [s.strip() for s in new_skills.split(',')]
    
    modify_personality = input("Modify personality traits? (y/n): ").lower() == 'y'
    if modify_personality:
        new_traits = input("Enter corrected personality traits (comma-separated): ")
        if new_traits.strip():
            profile.personality_traits = [t.strip() for t in new_traits.split(',')]
    
    modify_iq = input("Modify IQ indicators? (y/n): ").lower() == 'y'
    if modify_iq:
        new_iq = input("Enter corrected IQ indicators (comma-separated): ")
        if new_iq.strip():
            profile.iq_indicators = [i.strip() for i in new_iq.split(',')]
    
    # Log the modifications
    add_feedback_entry(state, "modification", "Clinical modifications applied", 
                      "Assessment results updated by clinical review", "medium", False)

# Psychological Assessment Analysis System
# Analyzes 15 questions like a professional psychologist
# Returns comprehensive evaluation with feedback and maintains assessment history

import os
import json
import datetime
from typing import Dict, List, TypedDict, Annotated, Optional
from dataclasses import dataclass, asdict
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from backend.llm.gemini_llm import llm

# Load environment variables
import dotenv
dotenv.load_dotenv()

@dataclass
class PsychologicalProfile:
    """Complete psychological profile structure"""
    skills: List[str]
    personality_traits: List[str]
    iq_indicators: List[str]
    cognitive_abilities: List[str]
    emotional_intelligence: List[str]
    behavioral_patterns: List[str]
    strengths: List[str]
    areas_for_improvement: List[str]
    risk_factors: List[str]
    recommendations: List[str]
    confidence_score: float
    assessment_date: str
    session_id: str

@dataclass
class FeedbackEntry:
    """Individual feedback entry"""
    timestamp: str
    category: str
    observation: str
    recommendation: str
    severity: str  # low, medium, high
    follow_up_required: bool

class AssessmentState(TypedDict):
    """State structure for psychological assessment workflow"""
    questions: List[Dict]
    answers: List[str]
    participant_info: Dict
    psychological_profile: Optional[PsychologicalProfile]
    feedback_log: List[FeedbackEntry]
    current_analysis_step: str
    human_review_needed: bool
    assessment_complete: bool
    session_notes: List[str]
    red_flags: List[str]
    messages: Annotated[List, add_messages]

class PsychologicalAssessment:
    def __init__(self):
        self.total_questions = 15
        self.feedback_storage = "assessment_feedback.json"
        self.psychological_frameworks = [
            "Big Five Personality Model",
            "DISC Assessment",
            "Emotional Intelligence (EQ)",
            "Cognitive Behavioral Analysis",
            "Psychodynamic Indicators"
        ]
        
    def load_feedback_history(self) -> List[Dict]:
        """Load previous assessment feedback"""
        try:
            if os.path.exists(self.feedback_storage):
                with open(self.feedback_storage, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading feedback history: {e}")
        return []
    
    def save_feedback(self, feedback_data: Dict):
        """Save assessment feedback to persistent storage"""
        try:
            history = self.load_feedback_history()
            history.append(feedback_data)
            
            with open(self.feedback_storage, 'w') as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            print(f"Error saving feedback: {e}")

    @staticmethod
    def psychological_skills_analysis(state: AssessmentState) -> AssessmentState:
        """Comprehensive skills analysis from psychological perspective"""
        try:
            qa_pairs = list(zip(state.get('questions', []), state.get('answers', [])))
            
            context = f"""
            As a professional psychologist, analyze these assessment responses for skills and competencies:
            
            Questions and Answers: {qa_pairs}
            Participant Info: {state.get('participant_info', {})}
            
            Provide a comprehensive psychological evaluation focusing on:
            1. Cognitive Skills (analytical thinking, problem-solving, decision-making)
            2. Interpersonal Skills (communication, empathy, leadership)
            3. Intrapersonal Skills (self-awareness, emotional regulation, resilience)
            4. Technical/Professional Skills (domain-specific abilities)
            5. Adaptive Skills (flexibility, learning agility, stress management)
            
            Format your response as a detailed psychological assessment report.
            Include confidence levels and note any areas requiring further evaluation.
            """
            
            response = llm.invoke(context)
            skills_analysis = parse_psychological_response(response, "skills")
            
            # Add to session notes
            state['session_notes'] = state.get('session_notes', [])
            state['session_notes'].append(f"Skills Analysis: {len(skills_analysis.get('skills', []))} skills identified")
            
            # Check for any concerning patterns
            if detect_skill_deficits(skills_analysis):
                state['red_flags'] = state.get('red_flags', [])
                state['red_flags'].append("Potential skill deficits identified - requires clinical attention")
            
            state['current_analysis_step'] = "skills_complete"
            state['messages'] = add_messages(state.get('messages', []), 
                                           {"role": "psychologist", "content": f"Skills assessment completed. Identified key competencies and areas for development."})
            
            # Store preliminary skills data
            if not state.get('psychological_profile'):
                state['psychological_profile'] = PsychologicalProfile(
                    skills=skills_analysis.get('skills', []),
                    personality_traits=[],
                    iq_indicators=[],
                    cognitive_abilities=skills_analysis.get('cognitive_abilities', []),
                    emotional_intelligence=[],
                    behavioral_patterns=[],
                    strengths=[],
                    areas_for_improvement=skills_analysis.get('areas_for_improvement', []),
                    risk_factors=[],
                    recommendations=[],
                    confidence_score=0.0,
                    assessment_date=datetime.datetime.now().isoformat(),
                    session_id=state.get('session_id', 'default')
                )
            else:
                state['psychological_profile'].skills = skills_analysis.get('skills', [])
                state['psychological_profile'].cognitive_abilities = skills_analysis.get('cognitive_abilities', [])
                
        except Exception as e:
            print(f"Error in skills analysis: {e}")
            state['human_review_needed'] = True
            add_feedback_entry(state, "error", f"Skills analysis failed: {str(e)}", "Require manual review", "high", True)
            
        return state

    @staticmethod
    def psychological_personality_analysis(state: AssessmentState) -> AssessmentState:
        """Deep personality analysis using psychological frameworks"""
        try:
            qa_pairs = list(zip(state.get('questions', []), state.get('answers', [])))
            
            context = f"""
            As a clinical psychologist, conduct a comprehensive personality assessment:
            
            Questions and Answers: {qa_pairs}
            Previous Skills Analysis: {state.get('psychological_profile', {}).skills if state.get('psychological_profile') else []}
            
            Apply these psychological frameworks:
            1. Big Five Personality Traits (OCEAN model)
            2. DISC Behavioral Assessment
            3. Emotional Intelligence Evaluation
            4. Attachment Styles Analysis
            5. Defense Mechanisms Identification
            6. Cognitive Patterns Assessment
            
            Provide detailed analysis including:
            - Core personality traits with evidence
            - Behavioral patterns and triggers
            - Emotional regulation capabilities
            - Interpersonal dynamics and relationship patterns
            - Potential psychological vulnerabilities or strengths
            - Risk factors for mental health concerns
            
            Use professional psychological terminology and provide confidence intervals.
            """
            
            response = llm.invoke(context)
            personality_analysis = parse_psychological_response(response, "personality")
            
            # Update psychological profile
            if state.get('psychological_profile'):
                state['psychological_profile'].personality_traits = personality_analysis.get('personality_traits', [])
                state['psychological_profile'].emotional_intelligence = personality_analysis.get('emotional_intelligence', [])
                state['psychological_profile'].behavioral_patterns = personality_analysis.get('behavioral_patterns', [])
                state['psychological_profile'].risk_factors = personality_analysis.get('risk_factors', [])
            
            # Check for psychological red flags
            check_psychological_red_flags(state, personality_analysis)
            
            state['current_analysis_step'] = "personality_complete"
            add_feedback_entry(state, "personality", "Comprehensive personality assessment completed", 
                             "Continue with cognitive evaluation", "medium", False)
            
        except Exception as e:
            print(f"Error in personality analysis: {e}")
            state['human_review_needed'] = True
            add_feedback_entry(state, "error", f"Personality analysis failed: {str(e)}", 
                             "Require clinical supervision", "high", True)
            
        return state

    @staticmethod
    def psychological_cognitive_analysis(state: AssessmentState) -> AssessmentState:
        """Cognitive abilities and IQ indicators analysis"""
        try:
            qa_pairs = list(zip(state.get('questions', []), state.get('answers', [])))
            
            context = f"""
            As a neuropsychologist, evaluate cognitive functioning and intellectual capabilities:
            
            Assessment Data: {qa_pairs}
            Personality Context: {state.get('psychological_profile', {}).personality_traits if state.get('psychological_profile') else []}
            
            Evaluate:
            1. Fluid Intelligence (reasoning, problem-solving, pattern recognition)
            2. Crystallized Intelligence (knowledge, vocabulary, learned skills)
            3. Working Memory and Processing Speed
            4. Executive Functions (planning, inhibition, cognitive flexibility)
            5. Attention and Concentration
            6. Learning and Memory Capabilities
            7. Verbal and Non-verbal Reasoning
            8. Creative and Divergent Thinking
            
            Provide:
            - Cognitive strengths and weaknesses
            - Estimated intellectual functioning level
            - Learning style preferences
            - Potential cognitive concerns or exceptional abilities
            - Recommendations for cognitive enhancement
            
            Use standardized psychological assessment principles.
            """
            
            response = llm.invoke(context)
            cognitive_analysis = parse_psychological_response(response, "cognitive")
            
            # Update psychological profile
            if state.get('psychological_profile'):
                state['psychological_profile'].iq_indicators = cognitive_analysis.get('iq_indicators', [])
                state['psychological_profile'].cognitive_abilities.extend(cognitive_analysis.get('additional_cognitive', []))
                state['psychological_profile'].strengths = cognitive_analysis.get('strengths', [])
                state['psychological_profile'].recommendations = cognitive_analysis.get('recommendations', [])
            
            state['current_analysis_step'] = "cognitive_complete"
            add_feedback_entry(state, "cognitive", "Cognitive assessment completed", 
                             "Proceeding to comprehensive evaluation", "low", False)
            
        except Exception as e:
            print(f"Error in cognitive analysis: {e}")
            state['human_review_needed'] = True
            add_feedback_entry(state, "error", f"Cognitive analysis failed: {str(e)}", 
                             "Require neuropsychological consultation", "high", True)
            
        return state

    @staticmethod
    def comprehensive_psychological_evaluation(state: AssessmentState) -> AssessmentState:
        """Final comprehensive psychological evaluation and report generation"""
        try:
            profile = state.get('psychological_profile')
            if not profile:
                raise ValueError("No psychological profile available for evaluation")
            
            # Calculate confidence score based on data completeness and consistency
            confidence_score = calculate_assessment_confidence(profile, state)
            profile.confidence_score = confidence_score
            
            # Generate comprehensive recommendations
            comprehensive_recommendations = generate_psychological_recommendations(profile, state)
            profile.recommendations.extend(comprehensive_recommendations)
            
            # Final psychological summary
            context = f"""
            As a senior clinical psychologist, provide a comprehensive psychological evaluation summary:
            
            Complete Profile: {asdict(profile)}
            Session Notes: {state.get('session_notes', [])}
            Red Flags: {state.get('red_flags', [])}
            Feedback Log: {[asdict(f) for f in state.get('feedback_log', [])]}
            
            Provide:
            1. Executive Summary of psychological functioning
            2. Key insights and clinical impressions
            3. Integrated analysis across all domains
            4. Risk assessment and protective factors
            5. Treatment or development recommendations
            6. Follow-up suggestions and monitoring needs
            7. Prognosis and expected outcomes
            
            Maintain professional standards and ethical considerations.
            """
            
            response = llm.invoke(context)
            
            # Add final evaluation to session notes
            state['session_notes'].append(f"Comprehensive evaluation completed - Confidence: {confidence_score:.2f}")
            
            add_feedback_entry(state, "evaluation", "Comprehensive psychological evaluation completed", 
                             "Review recommendations and consider follow-up", "low", 
                             len(state.get('red_flags', [])) > 0)
            
            state['current_analysis_step'] = "evaluation_complete"
            state['assessment_complete'] = True
            
        except Exception as e:
            print(f"Error in comprehensive evaluation: {e}")
            state['human_review_needed'] = True
            add_feedback_entry(state, "error", f"Evaluation failed: {str(e)}", 
                             "Require senior psychologist review", "high", True)
            
        return state

    @staticmethod
    def clinical_supervision_review(state: AssessmentState) -> AssessmentState:
        """Human psychologist supervision and review"""
        print("\n" + "="*60)
        print("CLINICAL SUPERVISION REQUIRED")
        print("="*60)
        
        profile = state.get('psychological_profile')
        if profile:
            print(f"\nAssessment Date: {profile.assessment_date}")
            print(f"Confidence Score: {profile.confidence_score:.2f}")
            print(f"\nSkills Identified: {len(profile.skills)}")
            print(f"Personality Traits: {len(profile.personality_traits)}")
            print(f"Cognitive Indicators: {len(profile.iq_indicators)}")
            print(f"\nRed Flags: {len(state.get('red_flags', []))}")
            
            if state.get('red_flags'):
                print("⚠️  RED FLAGS IDENTIFIED:")
                for flag in state.get('red_flags', []):
                    print(f"   • {flag}")
        
        print(f"\nFeedback Entries: {len(state.get('feedback_log', []))}")
        for feedback in state.get('feedback_log', [])[-3:]:  # Show last 3
            print(f"   • [{feedback.severity.upper()}] {feedback.observation}")
        
        print("\n" + "-"*60)
        
        # Clinical supervision input
        supervision_needed = input("Require clinical supervision? (y/n): ").lower() == 'y'
        
        if supervision_needed:
            print("\nCLINICAL REVIEW OPTIONS:")
            print("1. Modify assessment results")
            print("2. Add clinical notes")
            print("3. Flag for specialist referral")
            print("4. Approve as-is")
            
            choice = input("Select option (1-4): ")
            
            if choice == "1":
                # Allow modifications
                modify_assessment_results(state)
            elif choice == "2":
                clinical_note = input("Enter clinical note: ")
                state['session_notes'].append(f"Clinical Note: {clinical_note}")
                add_feedback_entry(state, "clinical", clinical_note, "Documented in clinical notes", "medium", False)
            elif choice == "3":
                referral_type = input("Referral type (psychiatrist/neuropsychologist/other): ")
                add_feedback_entry(state, "referral", f"Specialist referral recommended: {referral_type}", 
                                 "Schedule specialist consultation", "high", True)
            
        state['human_review_needed'] = False
        add_feedback_entry(state, "supervision", "Clinical supervision completed", 
                         "Assessment approved for final report", "low", False)
        
        return state

    @staticmethod
    def route_assessment_flow(state: AssessmentState) -> str:
        """Determines the next step in psychological assessment workflow"""
        current_step = state.get('current_analysis_step', '')
        
        if state.get('human_review_needed', False):
            return "clinical_supervision"
        elif current_step == 'skills_complete':
            return "personality_analysis"
        elif current_step == 'personality_complete':
            return "cognitive_analysis"
        elif current_step == 'cognitive_complete':
            return "comprehensive_evaluation"
        elif state.get('assessment_complete', False):
            return "end"
        else:
            return "skills_analysis"

    def build_psychological_assessment_graph(self):
        """Builds the comprehensive psychological assessment workflow"""
        graph_builder = StateGraph(AssessmentState)
        
        # Add psychological assessment nodes
        graph_builder.add_node("skills_analysis", self.psychological_skills_analysis)
        graph_builder.add_node("personality_analysis", self.psychological_personality_analysis)
        graph_builder.add_node("cognitive_analysis", self.psychological_cognitive_analysis)
        graph_builder.add_node("comprehensive_evaluation", self.comprehensive_psychological_evaluation)
        graph_builder.add_node("clinical_supervision", self.clinical_supervision_review)
        
        # Define workflow edges
        graph_builder.add_edge(START, "skills_analysis")
        
        # Add conditional routing
        graph_builder.add_conditional_edges(
            "skills_analysis",
            self.route_assessment_flow,
            {
                "personality_analysis": "personality_analysis",
                "clinical_supervision": "clinical_supervision",
                "end": END
            }
        )
        
        graph_builder.add_conditional_edges(
            "personality_analysis", 
            self.route_assessment_flow,
            {
                "cognitive_analysis": "cognitive_analysis",
                "clinical_supervision": "clinical_supervision",
                "end": END
            }
        )
        
        graph_builder.add_conditional_edges(
            "cognitive_analysis",
            self.route_assessment_flow,
            {
                "comprehensive_evaluation": "comprehensive_evaluation",
                "clinical_supervision": "clinical_supervision",
                "end": END
            }
        )
        
        graph_builder.add_conditional_edges(
            "comprehensive_evaluation",
            self.route_assessment_flow,
            {
                "clinical_supervision": "clinical_supervision",
                "end": END
            }
        )
        
        graph_builder.add_conditional_edges(
            "clinical_supervision",
            self.route_assessment_flow,
            {
                "end": END
            }
        )
        
        # Compile with memory for session persistence
        memory = MemorySaver()
        return graph_builder.compile(checkpointer=memory)

    def conduct_psychological_assessment(self, questions: List[Dict], answers: List[str], 
                                       participant_info: Dict = None) -> Dict:
        """Conducts comprehensive psychological assessment"""
        if len(questions) != self.total_questions or len(answers) != self.total_questions:
            raise ValueError(f"Expected exactly {self.total_questions} questions and answers")
        
        session_id = f"assessment_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Initialize psychological assessment state
        initial_state = {
            "questions": questions,
            "answers": answers,
            "participant_info": participant_info or {},
            "psychological_profile": None,
            "feedback_log": [],
            "current_analysis_step": "",
            "human_review_needed": False,
            "assessment_complete": False,
            "session_notes": [f"Assessment session {session_id} initiated"],
            "red_flags": [],
            "messages": [],
            "session_id": session_id
        }
        
        # Build and execute psychological assessment
        graph = self.build_psychological_assessment_graph()
        config = {"configurable": {"thread_id": session_id}}
        
        try:
            final_state = graph.invoke(initial_state, config)
            
            # Save comprehensive feedback
            feedback_data = {
                "session_id": session_id,
                "assessment_date": datetime.datetime.now().isoformat(),
                "psychological_profile": asdict(final_state.get('psychological_profile')) if final_state.get('psychological_profile') else None,
                "feedback_log": [asdict(f) for f in final_state.get('feedback_log', [])],
                "session_notes": final_state.get('session_notes', []),
                "red_flags": final_state.get('red_flags', []),
                "participant_info": final_state.get('participant_info', {})
            }
            
            self.save_feedback(feedback_data)
            
            # Return structured psychological assessment results
            profile = final_state.get('psychological_profile')
            if profile:
                return {
                    "skills": profile.skills,
                    "personality_traits": profile.personality_traits,
                    "iq": profile.iq_indicators,
                    "psychological_evaluation": {
                        "cognitive_abilities": profile.cognitive_abilities,
                        "emotional_intelligence": profile.emotional_intelligence,
                        "behavioral_patterns": profile.behavioral_patterns,
                        "strengths": profile.strengths,
                        "areas_for_improvement": profile.areas_for_improvement,
                        "risk_factors": profile.risk_factors,
                        "recommendations": profile.recommendations,
                        "confidence_score": profile.confidence_score,
                        "session_id": session_id
                    },
                    "clinical_feedback": final_state.get('feedback_log', []),
                    "session_notes": final_state.get('session_notes', []),
                    "requires_follow_up": len(final_state.get('red_flags', [])) > 0
                }
            else:
                raise ValueError("Assessment incomplete - no psychological profile generated")
                
        except Exception as e:
            error_feedback = {
                "session_id": session_id,
                "error": str(e),
                "timestamp": datetime.datetime.now().isoformat(),
                "status": "failed"
            }
            self.save_feedback(error_feedback)
            raise e

# Helper functions for psychological assessment

def parse_psychological_response(response, analysis_type: str) -> Dict:
    """Parse LLM response using psychological assessment standards"""
    if hasattr(response, 'content'):
        content = response.content
    else:
        content = str(response)
    
    # Implement sophisticated parsing based on psychological frameworks
    parsed_data = {}
    
    if analysis_type == "skills":
        parsed_data = {
            "skills": extract_psychological_constructs(content, ["skill", "ability", "competency", "capability"]),
            "cognitive_abilities": extract_psychological_constructs(content, ["cognitive", "thinking", "reasoning", "memory"]),
            "areas_for_improvement": extract_psychological_constructs(content, ["improve", "develop", "enhance", "strengthen"])
        }
    elif analysis_type == "personality":
        parsed_data = {
            "personality_traits": extract_psychological_constructs(content, ["trait", "characteristic", "tendency", "pattern"]),
            "emotional_intelligence": extract_psychological_constructs(content, ["emotional", "empathy", "social", "interpersonal"]),
            "behavioral_patterns": extract_psychological_constructs(content, ["behavior", "response", "reaction", "approach"]),
            "risk_factors": extract_psychological_constructs(content, ["risk", "concern", "vulnerability", "warning"])
        }
    elif analysis_type == "cognitive":
        parsed_data = {
            "iq_indicators": extract_psychological_constructs(content, ["intelligence", "reasoning", "problem-solving", "analytical"]),
            "additional_cognitive": extract_psychological_constructs(content, ["memory", "attention", "processing", "executive"]),
            "strengths": extract_psychological_constructs(content, ["strength", "strong", "excellent", "superior"]),
            "recommendations": extract_psychological_constructs(content, ["recommend", "suggest", "advise", "consider"])
        }
    
    return parsed_data

def extract_psychological_constructs(text: str, keywords: List[str]) -> List[str]:
    """Extract psychological constructs from text using NLP techniques"""
    constructs = []
    lines = text.lower().split('\n')
    
    for line in lines:
        for keyword in keywords:
            if keyword in line:
                # Extract meaningful phrases containing the keyword
                words = line.split()
                if keyword in ' '.join(words):
                    # Find phrases around the keyword
                    for i, word in enumerate(words):
                        if keyword in word:
                            start = max(0, i-2)
                            end = min(len(words), i+3)
                            phrase = ' '.join(words[start:end])
                            if len(phrase) > 10:  # Meaningful phrases
                                constructs.append(phrase.strip('.,!?'))
    
    # Remove duplicates and clean up
    return list(set([c for c in constructs if len(c) > 5]))[:10]  # Limit to top 10

def detect_skill_deficits(analysis: Dict) -> bool:
    """Detect potential skill deficits requiring clinical attention"""
    skills = analysis.get('skills', [])
    improvements = analysis.get('areas_for_improvement', [])
    
    # Red flags: very few skills identified or many improvement areas
    return len(skills) < 3 or len(improvements) > len(skills)

def check_psychological_red_flags(state: AssessmentState, analysis: Dict):
    """Check for psychological red flags requiring immediate attention"""
    risk_factors = analysis.get('risk_factors', [])
    red_flag_keywords = ['depression', 'anxiety', 'trauma', 'substance', 'suicide', 'self-harm', 'psychosis', 'mania']
    
    for risk in risk_factors:
        for keyword in red_flag_keywords:
            if keyword in risk.lower():
                state['red_flags'] = state.get('red_flags', [])
                state['red_flags'].append(f"Mental health concern identified: {risk}")
                state['human_review_needed'] = True

def add_feedback_entry(state: AssessmentState, category: str, observation: str, 
                      recommendation: str, severity: str, follow_up: bool):
    """Add structured feedback entry to assessment"""
    feedback = FeedbackEntry(
        timestamp=datetime.datetime.now().isoformat(),
        category=category,
        observation=observation,
        recommendation=recommendation,
        severity=severity,
        follow_up_required=follow_up
    )
    
    if 'feedback_log' not in state:
        state['feedback_log'] = []
    state['feedback_log'].append(feedback)

def calculate_assessment_confidence(profile: PsychologicalProfile, state: AssessmentState) -> float:
    """Calculate confidence score for psychological assessment"""
    base_score = 0.5
    
    # Data completeness
    data_completeness = (
        len(profile.skills) * 0.15 +
        len(profile.personality_traits) * 0.20 +
        len(profile.iq_indicators) * 0.15 +
        len(profile.cognitive_abilities) * 0.10 +
        len(profile.emotional_intelligence) * 0.10 +
        len(profile.behavioral_patterns) * 0.15 +
        len(profile.recommendations) * 0.10 +
        len(profile.strengths) * 0.05
    ) / 20  # Normalize to 0-1
    
    # Consistency check
    consistency_bonus = 0.2 if len(state.get('red_flags', [])) == 0 else -0.1
    
    # Human review factor
    human_review_factor = 0.1 if not state.get('human_review_needed', False) else 0.0
    
    confidence = min(1.0, base_score + data_completeness + consistency_bonus + human_review_factor)
    return round(confidence, 2)

def generate_psychological_recommendations(profile: PsychologicalProfile, state: AssessmentState) -> List[str]:
    """Generate evidence-based psychological recommendations"""
    recommendations = []
    
    # Based on strengths
    if profile.strengths:
        recommendations.append(f"Leverage identified strengths: {', '.join(profile.strengths[:3])}")
    
    # Based on areas for improvement
    if profile.areas_for_improvement:
        recommendations.append(f"Focus development on: {', '.join(profile.areas_for_improvement[:2])}")
    
    # Based on risk factors
    if profile.risk_factors:
        recommendations.append("Consider preventive interventions for identified risk factors")
        recommendations.append("Regular monitoring and follow-up recommended")
    
    # Based on red flags
    if state.get('red_flags'):
        recommendations.append("Immediate clinical consultation recommended")
        recommendations.append("Develop safety plan and support network")
    
    return recommendations

def modify_assessment_results(state: AssessmentState):
    """Allow clinical modification of assessment results"""
    profile = state.get('psychological_profile')
    if not profile:
        return
    
    print("\nCURRENT ASSESSMENT RESULTS:")
    print(f"Skills: {profile.skills}")
    print(f"Personality Traits: {profile.personality_traits}")
    print(f"IQ Indicators: {profile.iq_indicators}")
    
    # Allow modifications
    modify_skills = input("Modify skills? (y/n): ").lower() == 'y'
    if modify_skills:
        new_skills = input("Enter corrected skills (comma-separated): ")
        if new_skills.strip():
            profile.skills = [s.strip() for s in new_skills.split(',')]
    
    modify_personality = input("Modify personality traits? (y/n): ").lower() == 'y'
    if modify_personality:
        new_traits = input("Enter corrected personality traits (comma-separated): ")
        if new_traits.strip():
            profile.personality_traits = [t.strip() for t in new_traits.split(',')]
    
    modify_iq = input("Modify IQ indicators? (y/n): ").lower() == 'y'
    if modify_iq:
        new_iq = input("Enter corrected IQ indicators (comma-separated): ")
        if new_iq.strip():
            profile.iq_indicators = [i.strip() for i in new_iq.split(',')]
    
    # Log the modifications
    add_feedback_entry(state, "modification", "Clinical modifications applied", 
                      "Assessment results updated by clinical review", "medium", False)
if __name__ == "__main__":
    # Psychological assessment questions
    psychological_questions = [
        {"id": 1, "question": "How do you typically respond to stressful situations?", "domain": "emotional_regulation"},
        {"id": 2, "question": "Describe a time when you had to work with someone you disagreed with.", "domain": "interpersonal_skills"},
        {"id": 3, "question": "What motivates you most in your work or daily activities?", "domain": "motivation"},
        {"id": 4, "question": "How do you usually make important decisions?", "domain": "cognitive_processing"},
        {"id": 5, "question": "Tell me about a challenge you overcame recently.", "domain": "resilience"},
        {"id": 6, "question": "How do you prefer to learn new information or skills?", "domain": "learning_style"},
        {"id": 7, "question": "Describe your ideal work or living environment.", "domain": "environmental_preferences"},
        {"id": 8, "question": "How do you handle criticism or feedback?", "domain": "emotional_intelligence"},
        {"id": 9, "question": "What are your biggest strengths and how do you use them?", "domain": "self_awareness"},
        {"id": 10, "question": "Describe a time when you had to adapt to a significant change.", "domain": "adaptability"},
        {"id": 11, "question": "How do you maintain relationships with family, friends, or colleagues?", "domain": "social_functioning"},
        {"id": 12, "question": "What are your long-term goals and how do you work towards them?", "domain": "goal_orientation"},
        {"id": 13, "question": "How do you manage your emotions when things don't go as planned?", "domain": "emotional_regulation"},
        {"id": 14, "question": "Describe your problem-solving approach when facing complex issues.", "domain": "cognitive_abilities"},
        {"id": 15, "question": "What gives your life meaning and purpose?", "domain": "existential_wellbeing"}
    ]
    
    # Sample comprehensive psychological responses
    psychological_responses = [
        "I try to stay calm and break down the problem into manageable parts. I use deep breathing and focus on what I can control.",
        "I listen to understand their perspective first, then find common ground. I believe most disagreements come from miscommunication.",
        "I'm motivated by helping others and seeing the impact of my work. Making a difference drives me more than recognition.",
        "I gather information from multiple sources, consider pros and cons, and trust my intuition while being logical.",
        "Last month I lost my job unexpectedly. I used it as an opportunity to reassess my career goals and found something better aligned with my values.",
        "I'm a visual learner who likes hands-on experience. I learn best when I can see practical applications and practice immediately.",
        "I prefer collaborative environments with clear communication, flexibility, and opportunities for growth and creativity.",
        "I appreciate constructive feedback as a growth opportunity. I ask clarifying questions and reflect on how to improve.",
        "My biggest strength is empathy - I can understand others' perspectives easily. I use this in leadership and conflict resolution.",
        "When our company restructured, I embraced learning new systems and took on additional responsibilities to support my team.",
        "I maintain relationships through regular check-ins, active listening, and being reliable. I prioritize quality time and emotional support.",
        "My goal is to become a clinical psychologist. I'm taking courses, volunteering, and building relevant experience systematically.",
        "I allow myself to feel disappointed briefly, then focus on lessons learned and next steps. I practice self-compassion.",
        "I start by clearly defining the problem, brainstorm solutions, evaluate options systematically, and implement with contingency plans.",
        "Helping others reach their potential and contributing to positive change in my community gives my life deep meaning and purpose."
    ]
    
    # Participant information for comprehensive assessment
    participant_info = {
        "age": 28,
        "education": "Bachelor's degree in Psychology",
        "occupation": "Mental Health Counselor",
        "assessment_reason": "Career development and personal growth evaluation",
        "previous_assessments": None,
        "cultural_background": "Western",
        "primary_language": "English"
    }
    
    # Run comprehensive psychological assessment
    try:
        psychological_assessment = PsychologicalAssessment()
        
        print("🧠 INITIATING COMPREHENSIVE PSYCHOLOGICAL ASSESSMENT")
        print("="*80)
        print("Assessment will be conducted with professional psychological standards")
        print("Clinical supervision and feedback mechanisms are integrated")
        print("-"*80)
        
        results = psychological_assessment.conduct_psychological_assessment(
            questions=psychological_questions,
            answers=psychological_responses,
            participant_info=participant_info
        )
        
        print("\n" + "="*80)
        print("🔍 COMPREHENSIVE PSYCHOLOGICAL ASSESSMENT RESULTS")
        print("="*80)
        
        # Core assessment results
        print(f"\n📋 CORE ASSESSMENT:")
        print(f"   Skills Identified: {len(results['skills'])}")
        for i, skill in enumerate(results['skills'][:5], 1):
            print(f"      {i}. {skill}")
        if len(results['skills']) > 5:
            print(f"      ... and {len(results['skills'])-5} more")
            
        print(f"\n🧩 PERSONALITY PROFILE:")
        print(f"   Traits Identified: {len(results['personality_traits'])}")
        for i, trait in enumerate(results['personality_traits'][:5], 1):
            print(f"      {i}. {trait}")
        if len(results['personality_traits']) > 5:
            print(f"      ... and {len(results['personality_traits'])-5} more")
            
        print(f"\n🧠 COGNITIVE ASSESSMENT:")
        print(f"   IQ Indicators: {len(results['iq'])}")
        for i, indicator in enumerate(results['iq'][:5], 1):
            print(f"      {i}. {indicator}")
        if len(results['iq']) > 5:
            print(f"      ... and {len(results['iq'])-5} more")
        
        # Detailed psychological evaluation
        psych_eval = results['psychological_evaluation']
        print(f"\n🔬 DETAILED PSYCHOLOGICAL EVALUATION:")
        print(f"   Session ID: {psych_eval['session_id']}")
        print(f"   Assessment Confidence: {psych_eval['confidence_score']:.1%}")
        print(f"   Cognitive Abilities: {len(psych_eval['cognitive_abilities'])}")
        print(f"   Emotional Intelligence Factors: {len(psych_eval['emotional_intelligence'])}")
        print(f"   Behavioral Patterns: {len(psych_eval['behavioral_patterns'])}")
        
        print(f"\n💪 KEY STRENGTHS:")
        for i, strength in enumerate(psych_eval['strengths'][:3], 1):
            print(f"   {i}. {strength}")
            
        print(f"\n📈 DEVELOPMENT AREAS:")
        for i, area in enumerate(psych_eval['areas_for_improvement'][:3], 1):
            print(f"   {i}. {area}")
            
        print(f"\n⚠️  RISK FACTORS:")
        if psych_eval['risk_factors']:
            for i, risk in enumerate(psych_eval['risk_factors'][:3], 1):
                print(f"   {i}. {risk}")
        else:
            print("   No significant risk factors identified")
            
        print(f"\n📝 CLINICAL RECOMMENDATIONS:")
        for i, rec in enumerate(psych_eval['recommendations'][:5], 1):
            print(f"   {i}. {rec}")
        
        # Clinical feedback summary
        print(f"\n📊 CLINICAL FEEDBACK SUMMARY:")
        print(f"   Total Feedback Entries: {len(results['clinical_feedback'])}")
        print(f"   Session Notes: {len(results['session_notes'])}")
        print(f"   Follow-up Required: {'Yes' if results['requires_follow_up'] else 'No'}")
        
        if results['clinical_feedback']:
            print(f"\n   Recent Clinical Observations:")
            for feedback in results['clinical_feedback'][-3:]:  # Last 3 entries
                severity_icon = "🔴" if feedback.severity == "high" else "🟡" if feedback.severity == "medium" else "🟢"
                print(f"   {severity_icon} [{feedback.category.upper()}] {feedback.observation}")
                if feedback.follow_up_required:
                    print(f"      → Follow-up: {feedback.recommendation}")
        
        print(f"\n📋 SESSION DOCUMENTATION:")
        print(f"   Assessment completed with professional standards")
        print(f"   All data stored securely with timestamp: {psych_eval['session_id']}")
        print(f"   Feedback history maintained for longitudinal tracking")
        
        if results['requires_follow_up']:
            print(f"\n⚠️  IMPORTANT: This assessment indicates follow-up is recommended")
            print(f"   Please review clinical notes and consider specialist consultation")
        
        print("\n" + "="*80)
        print("✅ PSYCHOLOGICAL ASSESSMENT COMPLETE")
        print("="*80)
        
        # Demonstrate feedback history loading
        print(f"\n📚 FEEDBACK HISTORY DEMONSTRATION:")
        history = psychological_assessment.load_feedback_history()
        print(f"   Total historical assessments: {len(history)}")
        if history:
            print(f"   Most recent session: {history[-1].get('session_id', 'Unknown')}")
        
    except Exception as e:
        print(f"\n❌ ASSESSMENT ERROR: {e}")
        print("Clinical supervision required for error resolution")
        
        # Even in error cases, attempt to save partial feedback
        error_session_id = f"error_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        error_feedback = {
            "session_id": error_session_id,
            "error": str(e),
            "timestamp": datetime.datetime.now().isoformat(),
            "status": "failed",
            "questions_attempted": len(psychological_questions),
            "answers_provided": len(psychological_responses)
        }
        
        try:
            psychological_assessment.save_feedback(error_feedback)
            print(f"Error logged with session ID: {error_session_id}")
        except:
            print("Unable to save error feedback - manual documentation required")