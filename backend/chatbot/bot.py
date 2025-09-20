import asyncio
import json
import uuid
import os
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

# Disable LangSmith tracing to avoid 403 errors
os.environ["LANGCHAIN_TRACING_V2"] = "false"

from langchain.schema import BaseMessage, HumanMessage, AIMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain_core.tools import tool
from llm.gemini_llm import LLM_initialise

from langgraph.graph import StateGraph, END,START
# from langgraph.checkpoint.sqlite import SqliteSaver
# from langgraph.prebuilt import ToolExecutor

import pinecone
from pydantic import BaseModel, Field
from pydantic_schema.Enums import QuestionType,AssessmentType
from database.vector_db import VectorDatabase
from agents.main import CoordinatorSystem

from .Questions import PERSONALITY_QUESTIONS,PSYCHOMETRIC_QUESTIONS,APTITUDE_QUESTIONS

# ============================================================================
# MODELS AND ENUMS
# ============================================================================

class AssessmentState(BaseModel):
    """State for the assessment chatbot"""
    user_id: str
    session_id: str
    assessment_type: AssessmentType
    current_question_index: int = 0
    questions: List[Dict[str, Any]] = Field(default_factory=list)
    user_responses: List[Dict[str, Any]] = Field(default_factory=list)
    is_completed: bool = False
    report: Optional[str] = None
    context: Dict[str, Any] = Field(default_factory=dict)
    messages: List[BaseMessage] = Field(default_factory=list)
    waiting_for_input: bool = False  # NEW: Track if waiting for user input
    current_step: str = "start"  # NEW: Track current workflow step


@dataclass
class Question:
    id: str
    text: str
    type: QuestionType
    category: str
    options: Optional[List[str]] = None
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None

@dataclass
class UserResponse:
    question_id: str
    answer: str
    timestamp: datetime
    response_time_seconds: Optional[int] = None

ALL_QUESTIONS = {
    AssessmentType.PSYCHOMETRIC: PSYCHOMETRIC_QUESTIONS,
    AssessmentType.APTITUDE: APTITUDE_QUESTIONS,
    AssessmentType.PERSONALITY: PERSONALITY_QUESTIONS
}


class AssessmentRAG:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.vectorstore = None
        self._setup_vectorstore()
    
    def _setup_vectorstore(self):
        """Initialize vector store with assessment knowledge"""
        documents = []
        
        # Add question explanations and psychological theory
        for assessment_type, questions in ALL_QUESTIONS.items():
            for q in questions:
                doc_text = f"""
                Assessment Type: {assessment_type.value}
                Category: {q['category']}
                Question: {q['text']}
                Explanation: {q.get('explanation', 'No explanation provided')}
                """
                documents.append(doc_text)
        
        # Add psychological theory documents
        theory_docs = [
            """
            Big Five Personality Traits:
            1. Openness to Experience: creativity, curiosity, openness to new ideas
            2. Conscientiousness: organization, self-discipline, goal-directed behavior
            3. Extraversion: sociability, assertiveness, positive emotions
            4. Agreeableness: cooperation, trust, empathy
            5. Neuroticism: emotional instability, anxiety, negative emotions
            """,
            """
            MBTI Personality Types:
            - Extraversion (E) vs Introversion (I): Energy source and focus
            - Sensing (S) vs Intuition (N): Information gathering preference
            - Thinking (T) vs Feeling (F): Decision making approach
            - Judging (J) vs Perceiving (P): Lifestyle and work approach
            """,
            """
            Career Assessment Principles:
            - Aptitude tests measure potential for learning specific skills
            - Interest assessments identify preferred activities and environments
            - Personality tests reveal behavioral tendencies and preferences
            - Values assessments determine what's important to the individual
            """
        ]
        
        all_docs = documents + theory_docs
        splits = self.text_splitter.split_text('\n'.join(all_docs))
        
        self.vectorstore = VectorDatabase(self.embeddings).vector_store()
    
    def get_relevant_context(self, query: str, k: int = 3) -> List[str]:
        """Retrieve relevant context for question generation or analysis"""
        if not self.vectorstore:
            return []
        
        docs = self.vectorstore.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]

class AssessmentChatbot:
    def __init__(self):
        self.rag = AssessmentRAG()
        self.llm = LLM_initialise()
        self.setup_prompts()
    
    def setup_prompts(self):
        self.question_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert psychological assessor. Generate assessment questions based on the context provided.
            
            Context: {context}
            
            Generate questions that are:
            1. Psychologically valid and evidence-based
            2. Clear and unambiguous
            3. Appropriate for the assessment type: {assessment_type}
            4. Engaging and conversational
            
            Format your response as a single question with clear options if it's multiple choice."""),
            ("human", "Generate the next assessment question for category: {category}")
        ])
        
        self.analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert psychologist analyzing assessment responses.
            
            Context: {context}
            
            For each question-answer pair, provide:
            1. What the response indicates about the person
            2. Psychological interpretation
            3. Implications for career/personality profile
            
            Be professional, insightful, and constructive."""),
            ("human", "Analyze this response: Question: {question} | Answer: {answer}")
        ])
        
        self.report_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a psychological assessor creating a comprehensive report.
            
            Based on all the question-answer pairs and analyses provided, create a structured report in this EXACT format:
            
            [Question: [question text]
            Answer given by user: [user's answer]
            What it means: [psychological interpretation and implications]]
            
            [Question: [next question text]
            Answer given by user: [user's answer]  
            What it means: [psychological interpretation and implications]]
            
            ... continue for all questions ...
            
            SUMMARY:
            - Overall personality profile
            - Key strengths identified
            - Areas for development
            - Career recommendations based on assessment
            
            Context: {context}"""),
            ("human", "Create a comprehensive assessment report based on these responses: {responses}")
        ])

@tool
def get_next_question(state: AssessmentState) -> str:
    """Get the next question in the assessment"""
    questions = ALL_QUESTIONS[state.assessment_type]
    if state.current_question_index < len(questions):
        question = questions[state.current_question_index]
        return json.dumps(question)
    return "ASSESSMENT_COMPLETE"

@tool  
def analyze_response(question: str, answer: str, context: str) -> str:
    """Analyze a user's response to a question"""
    chatbot = AssessmentChatbot()
    analysis_chain = chatbot.analysis_prompt | chatbot.llm | StrOutputParser()
    
    relevant_context = chatbot.rag.get_relevant_context(f"{question} {answer}")
    context_str = "\n".join(relevant_context)
    
    return analysis_chain.invoke({
        "context": context_str,
        "question": question, 
        "answer": answer
    })

def start_assessment(state: AssessmentState) -> AssessmentState:
    """Initialize the assessment"""
    print(f"Starting assessment for {state.assessment_type.value}")
    
    questions = ALL_QUESTIONS[state.assessment_type]
    state.questions = questions
    state.current_question_index = 0
    state.current_step = "asking_question"
    
    # Get first question
    if questions:
        first_question = questions[0]
        question_text = f"Let's begin your {state.assessment_type.value} assessment.\n\n{first_question['text']}\n\n"
        if first_question.get('options'):
            question_text += f"Options:\n" + "\n".join(first_question['options'])
            
        state.messages.append(AIMessage(content=question_text))
        state.waiting_for_input = True
    
    return state

def ask_next_question(state: AssessmentState) -> AssessmentState:
    """Ask the next question in the assessment"""
    print(f"Asking question {state.current_question_index + 1}")
    
    if state.current_question_index < len(state.questions):
        next_question = state.questions[state.current_question_index]
        question_text = f"{next_question['text']}\n\n"
        if next_question.get('options'):
            question_text += f"Options:\n" + "\n".join(next_question['options'])
            
        state.messages.append(AIMessage(content=question_text))
        state.waiting_for_input = True
        state.current_step = "asking_question"
    else:
        state.is_completed = True
        state.current_step = "completed"
        state.messages.append(
            AIMessage(content="Thank you for completing the assessment! I'm now generating your personalized report...")
        )
    
    return state

def process_answer(state: AssessmentState) -> AssessmentState:
    """Process user's answer and move to next question"""
    print(f"Processing answer for question {state.current_question_index}")
    
    if not state.messages:
        return state
        
    # Find the last human message
    last_human_message = None
    for message in reversed(state.messages):
        if isinstance(message, HumanMessage):
            last_human_message = message
            break
    
    if last_human_message:
        # Store the user's response
        current_question = state.questions[state.current_question_index]
        response = {
            "question_id": current_question['id'],
            "question_text": current_question['text'],
            "answer": last_human_message.content,
            "timestamp": datetime.now().isoformat()
        }
        state.user_responses.append(response)
        
        # Move to next question
        state.current_question_index += 1
        state.waiting_for_input = False
        state.current_step = "processed_answer"
    
    return state

async def generate_report(state: AssessmentState) -> AssessmentState:
    """Generate the final assessment report"""
    print("Generating assessment report")
    
    if not state.user_responses:
        return state
    
    chatbot = AssessmentChatbot()
    
    # Analyze each response
    analyses = []
    for response in state.user_responses:
        analysis = analyze_response(
            response['question_text'],
            response['answer'], 
            f"Assessment type: {state.assessment_type.value}"
        )
        analyses.append({
            "question": response['question_text'],
            "answer": response['answer'],
            "analysis": analysis
        })
    
    # Generate comprehensive report
    report_chain = chatbot.report_prompt | chatbot.llm | StrOutputParser()
    relevant_context = chatbot.rag.get_relevant_context(
        f"{state.assessment_type.value} assessment personality analysis"
    )
    
    report = report_chain.invoke({
        "context": "\n".join(relevant_context),
        "responses": json.dumps(analyses, indent=2)
    })
    
    state.report = report
    state.current_step = "report_generated"
    state.messages.append(AIMessage(content="Your assessment report has been generated and sent to the coordinator agent."))

    coordinator_system = CoordinatorSystem()
    comprehensive_report = await coordinator_system.process_assessment_report(
        user_id=state.user_id,
        assessment_report=report,
        assessment_type=state.assessment_type
    )
    
    state.messages.append(AIMessage(content="Your comprehensive consultation report has been generated with psychological and career guidance."))
    state.comprehensive_consultation = comprehensive_report
    
    return state

def should_continue(state: AssessmentState) -> Literal["ask_next_question", "process_answer", "generate_report",END]:
    """Determine next step in the workflow"""
    print(f"Should continue check - Step: {state.current_step}, Question: {state.current_question_index}/{len(state.questions)}, Completed: {state.is_completed}")
    
    if state.current_step == "asking_question":
        # We just asked a question, now we need to wait for user input
        # This should not continue the workflow automatically
        return END
    elif state.current_step == "processed_answer":
        # We processed an answer, check if we need more questions
        if state.current_question_index < len(state.questions):
            return "ask_next_question"
        else:
            state.is_completed = True
            return "generate_report"
    elif state.current_step == "completed" and not state.report:
        return "generate_report"
    elif state.current_step == "report_generated":
        return END
    else:
        return END


def create_assessment_workflow():
    """Create the LangGraph workflow for assessment"""
    workflow = StateGraph(AssessmentState)
    
    # Add nodes
    workflow.add_node("start_assessment", start_assessment)
    workflow.add_node("ask_next_question", ask_next_question)
    workflow.add_node("process_answer", process_answer)  
    workflow.add_node("generate_report", generate_report)
    
    # Add edges
    workflow.set_entry_point("start_assessment")
    workflow.add_edge("start_assessment", END)  # Stop after first question
    
    # Process answer leads to conditional routing
    workflow.add_conditional_edges(
        "process_answer",
        should_continue,
        {
            "ask_next_question": "ask_next_question",
            "generate_report": "generate_report",
            END: END
        }
    )
    
    # After asking a question, stop and wait for input
    workflow.add_edge("ask_next_question", END)
    workflow.add_edge("generate_report", END)
    
    return workflow.compile()

#main
class AssessmentBot:
    def __init__(self):
        self.workflow = create_assessment_workflow()
        self.active_sessions = {}
    
    def _ensure_state_object(self, state_data) -> AssessmentState:
        """Convert dict to AssessmentState object if needed"""
        if isinstance(state_data, dict):
            # Handle the messages conversion properly
            messages = []
            if 'messages' in state_data:
                for msg_data in state_data['messages']:
                    if isinstance(msg_data, dict):
                        if msg_data.get('type') == 'human':
                            messages.append(HumanMessage(content=msg_data['content']))
                        elif msg_data.get('type') == 'ai':
                            messages.append(AIMessage(content=msg_data['content']))
                    else:
                        messages.append(msg_data)
                state_data['messages'] = messages
            
            return AssessmentState(**state_data)
        return state_data
    
    async def start_assessment(self, user_id: str, assessment_type: AssessmentType) -> tuple[str, str]:
        """Start a new assessment session"""
        session_id = str(uuid.uuid4())
        
        initial_state = AssessmentState(
            user_id=user_id,
            session_id=session_id,
            assessment_type=assessment_type
        )
        
        # Set recursion limit to prevent infinite loops
        config = {"recursion_limit": 10}
        result = await self.workflow.ainvoke(initial_state, config=config)
        
        # Convert dict back to AssessmentState object
        result_state = self._ensure_state_object(result)
        self.active_sessions[session_id] = result_state
        
        return session_id, result_state.messages[-1].content if result_state.messages else "Assessment started"
    
    async def process_user_input(self, session_id: str, user_input: str) -> str:
        """Process user input and return bot response"""
        if session_id not in self.active_sessions:
            return "Session not found. Please start a new assessment."
        
        # Ensure state is AssessmentState object
        state = self._ensure_state_object(self.active_sessions[session_id])
        
        # Add user message
        state.messages.append(HumanMessage(content=user_input))
        
        # Process the answer
        state = process_answer(state)
        
        # Continue workflow based on current state
        if state.current_step == "processed_answer":
            if state.current_question_index < len(state.questions):
                # Ask next question
                state = ask_next_question(state)
            else:
                # Generate report
                state.is_completed = True
                state = generate_report(state)
        
        self.active_sessions[session_id] = state
        
        return state.messages[-1].content if state.messages else "Processing..."
    
    def get_report(self, session_id: str) -> Optional[str]:
        """Get the final assessment report"""
        if session_id in self.active_sessions:
            state = self._ensure_state_object(self.active_sessions[session_id])
            return state.report
        return None
    
    def is_assessment_complete(self, session_id: str) -> bool:
        """Check if assessment is complete"""
        if session_id in self.active_sessions:
            state = self._ensure_state_object(self.active_sessions[session_id])
            return state.is_completed
        return False

# ============================================================================
# USAGE EXAMPLE
# ============================================================================

async def main():
    """Example usage of the assessment chatbot"""
    bot = AssessmentBot()
    
    # Start psychometric assessment
    user_id = "user_123"
    session_id, initial_response = await bot.start_assessment(user_id, AssessmentType.PSYCHOMETRIC)
    
    print(f"Bot: {initial_response}")
    
    # Simulate user responses
    sample_responses = [
        "A) Work alone and focus deeply",
        "4 - Agree", 
        "D) Use a combination of logic and intuition",
        "3 - Neutral",
        "B) Jump right in and learn by doing"
    ]
    
    for response in sample_responses:
        bot_response = await bot.process_user_input(session_id, response)
        print(f"User: {response}")
        print(f"Bot: {bot_response}")
        print("-" * 50)
    
    # Get final report
    if bot.is_assessment_complete(session_id):
        report = bot.get_report(session_id)
        print("FINAL REPORT:")
        print("=" * 50)
        print(report)

if __name__ == "__main__":
    asyncio.run(main())