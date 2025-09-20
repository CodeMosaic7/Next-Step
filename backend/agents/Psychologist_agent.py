import json

from llm.gemini_llm import LLM_initialise
from langchain.prompts import ChatPromptTemplate
from pydantic_schema.Enums import AssessmentType
from langchain.schema.output_parser import StrOutputParser

class PsychologistAgent:
    """Specialized agent for mental health analysis and support"""
    
    def __init__(self):
        self.llm = LLM_initialise()
        self.setup_prompts()
    
    def setup_prompts(self):
        self.analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a licensed clinical psychologist with expertise in psychological assessment analysis and mental health support.

Your role is to:
1. Analyze assessment reports for mental health indicators
2. Identify potential areas of concern (anxiety, stress, emotional regulation, etc.)
3. Recognize positive psychological traits and strengths
4. Provide evidence-based mental health recommendations
5. Suggest coping strategies and wellness practices

IMPORTANT GUIDELINES:
- Base your analysis on established psychological principles
- Look for patterns that indicate stress, anxiety, depression, or other mental health concerns
- Identify resilience factors and psychological strengths
- Provide constructive, supportive guidance
- Recommend professional help when appropriate
- Maintain ethical boundaries and confidentiality

Format your response with these sections:
1. MENTAL HEALTH INDICATORS
2. PSYCHOLOGICAL STRENGTHS
3. AREAS OF CONCERN
4. RECOMMENDED INTERVENTIONS
5. SELF-CARE STRATEGIES
6. PROFESSIONAL REFERRAL (if needed)"""),
            
            ("human", """Please analyze this assessment report for mental health indicators and provide psychological support recommendations:

ASSESSMENT TYPE: {assessment_type}
REPORT: {report}

Focus on psychological well-being, emotional regulation, stress factors, and mental health support needs.""")
        ])
        
        self.support_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are providing ongoing psychological support to a client based on their assessment results.

Provide personalized mental health guidance that includes:
- Specific coping strategies for identified concerns
- Mindfulness and stress management techniques  
- Emotional regulation exercises
- Building on psychological strengths
- Resources for continued support

Be empathetic, professional, and actionable in your recommendations."""),
            
            ("human", """Based on my analysis, provide detailed psychological support for: {concerns}

User's strengths to build upon: {strengths}
Assessment context: {context}""")
        ])

    async def analyze_report(self, report: str, assessment_type: AssessmentType) -> str:
        """Analyze assessment report from psychological perspective"""
        try:
            analysis_chain = self.analysis_prompt | self.llm | StrOutputParser()
            
            analysis = await analysis_chain.ainvoke({
                "report": report,
                "assessment_type": assessment_type.value
            })
            
            return analysis
            
        except Exception as e:
            return f"Error in psychological analysis: {str(e)}"
    
    async def extract_structured_data(self, analysis: str) -> Dict:
        """Extract structured psychological data for database storage"""
        try:
            extraction_chain = self.data_extraction_prompt | self.llm | StrOutputParser()
            
            result = await extraction_chain.ainvoke({
                "analysis": analysis
            })
            
            # Parse JSON response
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                # Return default structure if parsing fails
                return {
                    "personality_traits": {},
                    "mental_health_indicators": {
                        "stress_level": "medium",
                        "anxiety_indicators": [],
                        "resilience_factors": [],
                        "coping_mechanisms": []
                    },
                    "risk_factors": {
                        "severity": "low",
                        "areas_of_concern": [],
                        "needs_professional_help": False
                    },
                    "recommended_interventions": [],
                    "strengths": []
                }
                
        except Exception as e:
            print(f"Error extracting psychological data: {e}")
            return {}
    
    async def provide_support(self, concerns: str, strengths: str, context: str) -> str:
        """Provide detailed psychological support recommendations"""
        try:
            support_chain = self.support_prompt | self.llm | StrOutputParser()
            
            support = await support_chain.ainvoke({
                "concerns": concerns,
                "strengths": strengths,
                "context": context
            })
            
            return support
            
        except Exception as e:
            return f"Error providing psychological support: {str(e)}"
