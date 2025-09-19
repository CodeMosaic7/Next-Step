# Counsllor agent gets the following response from phsycologist agent
# Skills: ['analytical thinking', 'communication']
# Personality Traits: ['conscientious', 'open']
# IQ Indicators: ['high reasoning']
# Confidence Score: 85.00%
# Session ID: assessment_20250917_144748
# Follow-up Required: False

# based in this information it guides the student in finding right career path based current student status

from typing import List, Dict
from dataclasses import dataclass
from langgraph.graph import START, END, StateGraph

# Import your LLM wrapper (as in Psychologist_agent.py)
from backend.llm.gemini_llm import LLM_initialise

# -------------------------------------------------
# Step 1: Input structure from Psychologist Agent
# -------------------------------------------------
@dataclass
class AssessmentResult:
    skills: List[str]
    personality_traits: List[str]
    iq_indicators: List[str]
    confidence_score: float
    session_id: str
    follow_up_required: bool


# -------------------------------------------------
# Step 2: Counsellor Logic
# -------------------------------------------------
class CounsellorAgent:
    def __init__(self):
        # Initialise LLM once for efficiency
        self.llm = LLM_initialise()

    def generate_prompt(self, assessment: AssessmentResult) -> str:
        """
        Creates a context-rich prompt for the LLM
        """
        return f"""
You are an expert career counsellor.

The student has completed a psychological assessment. Here are the results:

- Skills: {assessment.skills}
- Personality Traits: {assessment.personality_traits}
- IQ Indicators: {assessment.iq_indicators}
- Confidence Score: {assessment.confidence_score}%
- Session ID: {assessment.session_id}
- Follow-up Required: {assessment.follow_up_required}

Task:
1. Suggest 3–5 suitable career paths based on their skills, traits, and IQ.
2. Explain WHY these careers fit the student's profile.
3. Suggest the next steps or roadmap (skills to learn, courses, internships).
4. Be concise, supportive, and practical.
"""
    
    def suggest_career_paths(self, assessment: AssessmentResult) -> Dict:
        # Build the LLM prompt
        prompt = self.generate_prompt(assessment)
        
        # Invoke the LLM
        response = self.llm.invoke(prompt)

        return {
            "session_id": assessment.session_id,
            "confidence_score": assessment.confidence_score,
            "career_guidance": response,
            "follow_up_required": assessment.follow_up_required
        }


# -------------------------------------------------
# Step 3: LangGraph State Setup
# -------------------------------------------------
@dataclass
class CounsellorState:
    assessment: AssessmentResult
    guidance: Dict = None


def counsellor_node(state: CounsellorState) -> CounsellorState:
    agent = CounsellorAgent()
    state.guidance = agent.suggest_career_paths(state.assessment)
    return state


# -------------------------------------------------
# Step 4: Build the Graph
# -------------------------------------------------
graph = StateGraph(CounsellorState)
graph.add_node("counsellor", counsellor_node)
graph.add_edge(START, "counsellor")
graph.add_edge("counsellor", END)

compiled_graph = graph.compile()


# -------------------------------------------------
# Step 5: Test Run
# -------------------------------------------------
if __name__ == "__main__":
    sample_assessment = AssessmentResult(
        skills=['analytical thinking', 'communication'],
        personality_traits=['conscientious', 'open'],
        iq_indicators=['high reasoning'],
        confidence_score=85.00,
        session_id="assessment_20250917_144748",
        follow_up_required=False
    )

    final_state = compiled_graph.invoke(CounsellorState(assessment=sample_assessment))
    print(final_state.guidance["career_guidance"])
