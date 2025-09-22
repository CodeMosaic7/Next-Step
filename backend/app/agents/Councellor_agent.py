import json
from typing import Dict
from app.llm.gemini_llm import LLM_initialise
from langchain.prompts import ChatPromptTemplate
from app.pydantic_schema.Enums import AssessmentType
from langchain.schema.output_parser import StrOutputParser


class CounsellorAgent:
    """Specialized agent for career guidance and professional development"""

    def __init__(self):
        self.llm = LLM_initialise()
        self.setup_prompts()

    def setup_prompts(self):
        self.guidance_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a professional career counsellor with expertise in career development, job market analysis, and professional growth.

Your role is to:
1. Analyze assessment reports for career-relevant traits and abilities
2. Identify suitable career paths and opportunities
3. Recognize professional strengths and development areas
4. Provide actionable career development recommendations
5. Suggest skills development and learning opportunities

GUIDELINES:
- Base recommendations on current job market trends
- Consider personality traits, aptitudes, and interests
- Provide specific, actionable career advice
- Include both short-term and long-term career planning
- Suggest relevant skills, certifications, or education
- Consider work-life balance and job satisfaction factors

Format your response with these sections:
1. CAREER PERSONALITY PROFILE
2. RECOMMENDED CAREER PATHS
3. PROFESSIONAL STRENGTHS
4. SKILLS TO DEVELOP
5. ACTION PLAN (Short & Long term)
6. RESOURCES AND NEXT STEPS"""),

            ("human", """Please analyze this assessment report and provide comprehensive career guidance:

ASSESSMENT TYPE: {assessment_type}
REPORT: {report}

Focus on career fit, professional development, skill recommendations, and actionable career planning advice.""")
        ])

        self.career_data_extraction_prompt = ChatPromptTemplate.from_messages([
            ("system", """Extract structured career guidance data for database storage as JSON:

{
    "career_recommendations": [
        {
            "career_path": {
                "title": "Career Title",
                "industry": "Industry Name",
                "description": "Brief description",
                "required_skills": ["skill1", "skill2"],
                "personality_traits": {"trait": "description"},
                "salary_range": {"min": 50000, "max": 80000, "currency": "USD"},
                "growth_prospects": "High/Medium/Low",
                "education_requirements": ["degree", "certification"],
                "experience_requirements": "0-2 years"
            },
            "match_score": 0.85,
            "reasoning": "Why this career matches",
            "priority_level": "high/medium/low"
        }
    ],
    "identified_skills": [
        {
            "skill_name": "Skill Name",
            "category": "technical/soft/domain-specific",
            "proficiency_level": "beginner/intermediate/advanced",
            "description": "Skill description",
            "industry_relevance": ["industry1", "industry2"]
        }
    ],
    "skill_gap_analysis": {
        "strengths": ["existing skills"],
        "gaps": ["skills to develop"],
        "priority_skills": ["most important skills to learn"]
    },
    "action_plan": {
        "short_term": ["actions for next 3-6 months"],
        "long_term": ["actions for 1-2 years"],
        "resources": ["learning resources", "certifications"]
    },
    "career_preferences": {
        "work_environment": "remote/office/hybrid",
        "team_size": "small/medium/large",
        "leadership_interest": true/false,
        "entrepreneurial_interest": true/false
    }
}

Only include data that can be reasonably inferred from the career analysis."""),

            ("human", "Extract structured career data from this analysis: {analysis}")
        ])

        self.development_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are providing personalized career development guidance based on assessment results.

Create a detailed professional development plan that includes:
- Specific skills to develop
- Learning resources and courses
- Networking strategies
- Career advancement tactics
- Industry-specific advice
- Timeline for career goals

Be practical, specific, and motivating in your guidance."""),

            ("human", """Create a detailed career development plan for someone with these traits: {traits}

Recommended career paths: {career_paths}
Current context: {context}""")
        ])

    async def provide_guidance(self, report: str, assessment_type: AssessmentType) -> str:
        """Provide comprehensive career guidance based on assessment"""
        try:
            guidance_chain = self.guidance_prompt | self.llm | StrOutputParser()

            guidance = await guidance_chain.ainvoke({
                "report": report,
                "assessment_type": assessment_type.value
            })

            return guidance

        except Exception as e:
            return f"Error in career guidance: {str(e)}"

    async def extract_career_data(self, analysis: str) -> Dict:
        """Extract structured career data for database storage"""
        try:
            extraction_chain = self.career_data_extraction_prompt | self.llm | StrOutputParser()

            result = await extraction_chain.ainvoke({
                "analysis": analysis
            })

            # Parse JSON response
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                # Return default structure if parsing fails
                return {
                    "career_recommendations": [],
                    "identified_skills": [],
                    "skill_gap_analysis": {
                        "strengths": [],
                        "gaps": [],
                        "priority_skills": []
                    },
                    "action_plan": {
                        "short_term": [],
                        "long_term": [],
                        "resources": []
                    },
                    "career_preferences": {}
                }

        except Exception as e:
            print(f"Error extracting career data: {e}")
            return {}

    async def create_development_plan(self, traits: str, career_paths: str, context: str) -> str:
        """Create detailed professional development plan"""
        try:
            development_chain = self.development_prompt | self.llm | StrOutputParser()

            plan = await development_chain.ainvoke({
                "traits": traits,
                "career_paths": career_paths,
                "context": context
            })

            return plan

        except Exception as e:
            return f"Error creating development plan: {str(e)}"
