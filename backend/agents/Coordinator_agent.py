import json
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema import BaseMessage
from pydantic import BaseModel,Field
from typing import Optional, List, Dict, Any

from .Councellor_agent import CounsellorAgent
from .Psychologist_agent import PsychologistAgent
from llm.gemini_llm import LLM_initialise
from pydantic_schema.Enums import AssessmentType,SupportType,ConsultationStatus

class CoordinatorAgent:
    """Main coordinator that manages communication between specialized agents"""
    
    def __init__(self):
        self.llm = LLM_initialise()
        self.psychologist = PsychologistAgent()
        self.counsellor = CounsellorAgent()
        self.setup_prompts()
    
    def setup_prompts(self):
        self.triage_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a coordination specialist who routes assessment reports to appropriate support services.

Analyze the assessment report and determine:
1. Does this person need mental health support? (anxiety, stress, emotional concerns)
2. Does this person need career guidance? (career planning, professional development)
3. What should be the priority focus?

Respond with a JSON object:
{
    "needs_mental_health": true/false,
    "needs_career_guidance": true/false,
    "priority": "mental_health" | "career_guidance" | "both",
    "urgency": "low" | "medium" | "high",
    "reasoning": "explanation of the decision"
}"""),
            
            ("human", "Analyze this assessment report and determine support needs: {report}")
        ])
        
        self.synthesis_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are creating a comprehensive consultation report by synthesizing inputs from psychological and career guidance specialists.

Combine the analyses to create:
1. Executive Summary
2. Key Findings (psychological + career)
3. Integrated Recommendations
4. Priority Actions
5. Resources and Next Steps

Make the report cohesive, actionable, and user-friendly."""),
            
            ("human", """Create a comprehensive report combining these analyses:

PSYCHOLOGICAL ANALYSIS:
{psychological_analysis}

CAREER GUIDANCE:
{career_guidance}

ASSESSMENT TYPE: {assessment_type}
USER CONTEXT: Make this personal and actionable.""")
        ])

    async def analyze_support_needs(self, report: str) -> Dict[str, Any]:
        """Determine what type of support the user needs"""
        try:
            # Format the prompt manually since LLM might not support chain operations
            formatted_prompt = self.triage_prompt.format(report=report)
            
            # Call LLM directly if it doesn't support chain operations
            if hasattr(self.llm, 'invoke'):
                result = await self.llm.ainvoke(formatted_prompt)
            elif hasattr(self.llm, 'generate'):
                result = await self.llm.generate(formatted_prompt)
            elif callable(self.llm):
                result = await self.llm(formatted_prompt)
            else:
                # Fallback for sync methods
                result = self.llm.generate(formatted_prompt) if hasattr(self.llm, 'generate') else str(self.llm(formatted_prompt))
            
            # Parse JSON response
            try:
                support_needs = json.loads(result)
                return support_needs
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return {
                    "needs_mental_health": True,
                    "needs_career_guidance": True,
                    "priority": "both",
                    "urgency": "medium",
                    "reasoning": "Default routing due to parsing error"
                }
                
        except Exception as e:
            # Default to providing both types of support
            return {
                "needs_mental_health": True,
                "needs_career_guidance": True,
                "priority": "both",
                "urgency": "medium",
                "reasoning": f"Error in analysis: {str(e)}"
            }

    async def synthesize_reports(self, psychological_analysis: str, career_guidance: str, assessment_type: AssessmentType) -> str:
        """Combine psychological and career analyses into comprehensive report"""
        try:
            synthesis_chain = self.synthesis_prompt | self.llm | StrOutputParser()
            
            comprehensive_report = await synthesis_chain.ainvoke({
                "psychological_analysis": psychological_analysis,
                "career_guidance": career_guidance,
                "assessment_type": assessment_type.value
            })
            
            return comprehensive_report
            
        except Exception as e:
            return f"Error synthesizing reports: {str(e)}"
