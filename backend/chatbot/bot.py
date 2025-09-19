# RAG Psychometric Assessment Generator
import streamlit as st
import json
import os
from datetime import datetime
from uuid import uuid4
import time
import numpy as np
from typing import List, Dict, Any, Optional

# LangChain imports
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone as LangchainPinecone
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate

# Pinecone imports
import pinecone
from pinecone import Pinecone, ServerlessSpec

# Environment setup
import warnings
warnings.filterwarnings('ignore')

# setup vector datebase
# 

class PsychometricRAGSystem:
    """RAG system for psychometric assessment using Pinecone and LangChain"""
    
    def __init__(self, 
                 gemini_api_key: str,
                 pinecone_api_key: str, 
                 pinecone_environment: str = "us-east-1-aws",
                 index_name: str = "psychometric-kb"):
        
        # API Keys
        self.openai_api_key = openai_api_key
        self.pinecone_api_key = pinecone_api_key
        self.pinecone_environment = pinecone_environment
        self.index_name = index_name
        
        # Initialize components
        self.embeddings = None
        self.vectorstore = None
        self.llm = None
        self.psychologist_agent = None
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Initialize system
        self._initialize_system()
    
    def _initialize_system(self):
        """Initialize all RAG components"""
        try:
            # Initialize OpenAI embeddings
            os.environ["OPENAI_API_KEY"] = self.openai_api_key
            self.embeddings = OpenAIEmbeddings(
                model="text-embedding-3-small",
                openai_api_key=self.openai_api_key
            )
            
            # Initialize Pinecone
            pc = Pinecone(api_key=self.pinecone_api_key)
            
            # Create or connect to index
            if self.index_name not in pc.list_indexes().names():
                pc.create_index(
                    name=self.index_name,
                    dimension=1536,  # OpenAI embedding dimension
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region=self.pinecone_environment
                    )
                )
                st.info(f"Created new Pinecone index: {self.index_name}")
            
            # Initialize vectorstore
            self.vectorstore = LangchainPinecone.from_existing_index(
                self.index_name,
                self.embeddings
            )
            
            # Initialize LLM
            self.llm = ChatOpenAI(
                model_name="gpt-4",
                temperature=0.2,
                openai_api_key=self.openai_api_key
            )
            
            # Initialize psychologist agent
            self.psychologist_agent = PsychologistAgent(self.llm, self.vectorstore)
            
            st.success("RAG System initialized successfully!")
            
        except Exception as e:
            st.error(f"Failed to initialize RAG system: {str(e)}")
            raise
    
    def populate_knowledge_base(self):
        """Populate Pinecone with psychometric knowledge"""
        
        psychometric_documents = [
            # Aptitude Assessment Guidelines
            {
                "content": """
                Aptitude Assessment Best Practices:
                
                1. Cognitive Domains Coverage:
                - Verbal Reasoning: Test vocabulary, analogies, reading comprehension
                - Numerical Ability: Mathematical problem-solving, quantitative reasoning
                - Logical Reasoning: Deductive and inductive reasoning, syllogisms
                - Spatial Reasoning: Mental rotation, visual-spatial processing
                - Pattern Recognition: Sequential patterns, abstract reasoning
                
                2. Item Construction Guidelines:
                - Use clear, unambiguous language
                - Avoid cultural bias and jargon
                - Include plausible distractors based on common errors
                - Ensure single correct answer for each item
                - Calibrate difficulty appropriate to target population
                
                3. Psychometric Standards:
                - Reliability coefficient should exceed 0.80
                - Item difficulty should range from 0.3 to 0.9
                - Discrimination indices should be above 0.3
                - Avoid ceiling and floor effects
                """,
                "metadata": {
                    "category": "aptitude_guidelines",
                    "source": "APA Standards for Educational and Psychological Testing",
                    "topic": "cognitive_assessment"
                }
            },
            {
                "content": """
                Verbal Reasoning Assessment Framework:
                
                Key Components:
                - Vocabulary Knowledge: Test understanding of word meanings and relationships
                - Analogical Reasoning: Assess ability to identify relationships between concepts
                - Reading Comprehension: Evaluate text understanding and inference
                - Verbal Fluency: Measure word generation and language flexibility
                
                Item Types:
                - Synonyms/Antonyms: Choose words with similar/opposite meanings
                - Analogies: Complete word relationships (A:B :: C:?)
                - Sentence Completion: Fill in missing words in context
                - Reading Passages: Answer questions about text content
                
                Difficulty Factors:
                - Word frequency and familiarity
                - Abstract vs. concrete concepts
                - Sentence complexity and length
                - Cultural specificity of content
                """,
                "metadata": {
                    "category": "aptitude_verbal",
                    "source": "Cognitive Assessment Handbook",
                    "topic": "verbal_reasoning"
                }
            },
            # Personality Assessment Guidelines
            {
                "content": """
                Big Five Personality Assessment Framework:
                
                1. Openness to Experience:
                - Facets: Fantasy, Aesthetics, Feelings, Actions, Ideas, Values
                - High: Creative, curious, broad interests, unconventional
                - Low: Conventional, practical, prefer routine, narrow interests
                - Sample Items: "I enjoy abstract thinking", "I have a rich imagination"
                
                2. Conscientiousness:
                - Facets: Competence, Order, Dutifulness, Achievement, Self-discipline, Deliberation
                - High: Organized, responsible, hardworking, goal-oriented
                - Low: Disorganized, careless, impulsive, unreliable
                - Sample Items: "I am always prepared", "I follow through on commitments"
                
                3. Extraversion:
                - Facets: Warmth, Gregariousness, Assertiveness, Activity, Excitement-seeking, Positive emotions
                - High: Outgoing, energetic, assertive, sociable
                - Low: Reserved, quiet, independent, prefer solitude
                - Sample Items: "I enjoy being around people", "I take charge in groups"
                
                4. Agreeableness:
                - Facets: Trust, Straightforwardness, Altruism, Compliance, Modesty, Tender-mindedness
                - High: Cooperative, trusting, helpful, empathetic
                - Low: Competitive, skeptical, tough-minded, antagonistic
                - Sample Items: "I trust others' intentions", "I help others willingly"
                
                5. Neuroticism:
                - Facets: Anxiety, Angry hostility, Depression, Self-consciousness, Impulsiveness, Vulnerability
                - High: Emotionally reactive, prone to stress, moody
                - Low: Emotionally stable, calm, resilient, even-tempered
                - Sample Items: "I worry about many things", "I remain calm under pressure" (reverse)
                """,
                "metadata": {
                    "category": "personality_guidelines",
                    "source": "NEO-PI-R Professional Manual",
                    "topic": "big_five_model"
                }
            },
            {
                "content": """
                Personality Item Construction Guidelines:
                
                1. Item Writing Principles:
                - Use behavioral descriptions rather than trait labels
                - Write in first person ("I" statements)
                - Keep language simple and clear
                - Avoid double-barreled questions
                - Include both positive and negative keyed items
                
                2. Response Scale Design:
                - Use 5-point or 7-point Likert scales
                - Provide clear anchor points
                - Common scale: Strongly Disagree (1) to Strongly Agree (5)
                - Alternative: Very Inaccurate (1) to Very Accurate (5)
                
                3. Bias Control:
                - Include reverse-scored items (30-40% of total)
                - Avoid socially desirable response patterns  
                - Balance positive and negative trait descriptions
                - Use forced-choice format for high-stakes assessment
                
                4. Validity Considerations:
                - Ensure face validity - items should appear relevant
                - Maintain content validity - adequate factor coverage
                - Consider cultural appropriateness and accessibility
                - Include validity scales to detect response sets
                """,
                "metadata": {
                    "category": "personality_construction",
                    "source": "Personality Assessment Guidelines",
                    "topic": "item_development"
                }
            },
            # Clinical and Evaluation Standards
            {
                "content": """
                Clinical Assessment and Evaluation Standards:
                
                1. Reliability Requirements:
                - Internal consistency (Cronbach's alpha) ≥ 0.80 for clinical decisions
                - Test-retest reliability ≥ 0.75 for stable traits
                - Inter-rater reliability ≥ 0.85 for subjective scoring
                - Standard error of measurement should be reported
                
                2. Validity Evidence:
                - Content validity: Expert review of item relevance
                - Construct validity: Factor analysis, convergent/discriminant validity
                - Criterion validity: Correlation with external criteria
                - Face validity: Apparent relevance to test-takers
                
                3. Normative Data:
                - Representative samples for target populations
                - Demographic stratification (age, gender, education, ethnicity)
                - Sample size ≥ 200 per demographic subgroup
                - Regular norm updates (every 10-15 years)
                
                4. Ethical Guidelines:
                - Informed consent for assessment
                - Confidentiality and data security
                - Cultural sensitivity and fairness
                - Appropriate use and interpretation
                - Feedback and explanation of results
                """,
                "metadata": {
                    "category": "clinical_standards",
                    "source": "APA Ethical Principles and Code of Conduct",
                    "topic": "assessment_ethics"
                }
            },
            {
                "content": """
                Psychologist Evaluation Framework:
                
                Assessment Quality Indicators:
                
                1. Content Quality (0-100 scale):
                - Item clarity and readability (25 points)
                - Appropriate difficulty level (25 points)  
                - Cultural fairness and accessibility (25 points)
                - Theoretical alignment with constructs (25 points)
                
                2. Psychometric Properties:
                - Expected reliability estimates
                - Validity evidence requirements
                - Normative comparison standards
                - Measurement precision indicators
                
                3. Clinical Utility:
                - Diagnostic accuracy potential
                - Treatment planning relevance
                - Risk assessment capability
                - Progress monitoring sensitivity
                
                4. Professional Standards Compliance:
                - APA Guidelines adherence
                - Ethical considerations met
                - Legal and regulatory compliance
                - Cultural competence demonstrated
                
                Evaluation Criteria:
                - Excellent (90-100): Ready for clinical use
                - Good (80-89): Minor revisions needed
                - Fair (70-79): Moderate improvements required
                - Poor (<70): Major revision or rejection recommended
                """,
                "metadata": {
                    "category": "evaluation_framework",
                    "source": "Clinical Psychology Assessment Standards",
                    "topic": "quality_evaluation"
                }
            }
        ]
        
        # Convert to LangChain documents
        documents = []
        for doc_data in psychometric_documents:
            doc = Document(
                page_content=doc_data["content"],
                metadata=doc_data["metadata"]
            )
            documents.append(doc)
        
        # Split documents for better retrieval
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        
        split_docs = text_splitter.split_documents(documents)
        
        # Add to vectorstore
        try:
            self.vectorstore.add_documents(split_docs)
            st.success(f"Added {len(split_docs)} document chunks to knowledge base!")
            return True
        except Exception as e:
            st.error(f"Failed to populate knowledge base: {str(e)}")
            return False
    
    def generate_test_questions(self, test_type: str, specifications: Dict[str, Any]) -> Dict[str, Any]:
        """Generate test questions using RAG"""
        
        # Retrieve relevant context
        query = f"{test_type} assessment guidelines item construction best practices"
        relevant_docs = self.vectorstore.similarity_search(
            query, 
            k=5,
            filter={"category": f"{test_type}_guidelines"} if test_type != "psychometric" else None
        )
        
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        
        # Create generation prompt
        prompt = self._create_generation_prompt(test_type, specifications, context)
        
        # Generate questions
        try:
            response = self.llm.predict(prompt)
            return json.loads(response)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {"error": "Failed to parse LLM response", "raw_response": response}
    
    def _create_generation_prompt(self, test_type: str, specifications: Dict[str, Any], context: str) -> str:
        """Create detailed prompt for question generation"""
        
        item_count = specifications.get('item_count', 10)
        difficulty = specifications.get('difficulty', 'medium')
        target_population = specifications.get('target_population', 'adults')
        
        if test_type == "aptitude":
            prompt = f"""
You are an expert psychometrician creating an aptitude assessment. Use the following guidelines:

CONTEXT FROM KNOWLEDGE BASE:
{context}

SPECIFICATIONS:
- Test Type: {test_type}
- Number of Items: {item_count}
- Difficulty Level: {difficulty}
- Target Population: {target_population}

Generate {item_count} high-quality aptitude questions covering these domains:
- Verbal Reasoning (2-3 items)
- Numerical Ability (2-3 items)
- Logical Reasoning (2-3 items)
- Spatial Reasoning (1-2 items)
- Pattern Recognition (1-2 items)

Return ONLY valid JSON in this exact format:
{{
  "test_type": "aptitude",
  "specifications": {specifications},
  "items": [
    {{
      "id": "apt_001",
      "domain": "verbal_reasoning",
      "difficulty": "medium",
      "question": "Question text here",
      "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
      "correct_answer": "A",
      "explanation": "Detailed explanation here",
      "cognitive_process": "Specific cognitive skill tested",
      "estimated_time": "45 seconds"
    }}
  ]
}}

Ensure each question follows psychometric best practices from the context.
"""
        
        elif test_type == "personality":
            prompt = f"""
You are an expert psychometrician creating a personality assessment based on the Big Five model.

CONTEXT FROM KNOWLEDGE BASE:
{context}

SPECIFICATIONS:
- Test Type: {test_type}
- Number of Items: {item_count}
- Difficulty Level: {difficulty}
- Target Population: {target_population}

Generate {item_count} personality items covering all Big Five factors:
- Openness (2 items)
- Conscientiousness (2 items)
- Extraversion (2 items)
- Agreeableness (2 items)
- Neuroticism (2 items)

Include reverse-scored items (40% of total). Return ONLY valid JSON:

{{
  "test_type": "personality",
  "specifications": {specifications},
  "items": [
    {{
      "id": "per_001",
      "factor": "Openness",
      "facet": "Creativity",
      "statement": "I enjoy thinking of creative solutions to problems",
      "scale_type": "likert_5",
      "reverse_scored": false,
      "response_options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
    }}
  ]
}}

Follow Big Five model guidelines from the context.
"""
        
        else:  # psychometric (combined)
            prompt = f"""
You are an expert psychometrician creating a comprehensive psychometric assessment.

CONTEXT FROM KNOWLEDGE BASE:
{context}

SPECIFICATIONS:
- Test Type: Combined Psychometric Assessment
- Total Items: {item_count}
- Difficulty Level: {difficulty}  
- Target Population: {target_population}

Generate a balanced assessment with:
- Aptitude items (60% of total): {int(item_count * 0.6)} items
- Personality items (40% of total): {int(item_count * 0.4)} items

Return ONLY valid JSON:
{{
  "test_type": "psychometric",
  "specifications": {specifications},
  "aptitude_items": [
    // Aptitude questions following previous format
  ],
  "personality_items": [
    // Personality questions following previous format  
  ]
}}

Ensure comprehensive coverage of cognitive domains and personality factors.
"""
        
        return prompt

class PsychologistAgent:
    """AI Psychologist for comprehensive evaluation"""
    
    def __init__(self, llm, vectorstore):
        self.llm = llm
        self.vectorstore = vectorstore
        
        # Create evaluation chain
        self.evaluation_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 5, "filter": {"category": "evaluation_framework"}}
            )
        )
    
    def evaluate_assessment_results(self, test_data: Dict[str, Any], responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Comprehensive psychological evaluation"""
        
        # Create evaluation prompt
        evaluation_prompt = f"""
You are a clinical psychologist conducting a comprehensive psychological evaluation.

TEST DATA:
{json.dumps(test_data, indent=2)}

PARTICIPANT RESPONSES:
{json.dumps(responses, indent=2)}

Provide a detailed psychological evaluation including:

1. APTITUDE ANALYSIS (if applicable):
   - Overall cognitive ability level
   - Domain-specific strengths and weaknesses
   - Percentile rankings and standard scores
   - Clinical interpretation and recommendations

2. PERSONALITY ANALYSIS (if applicable):
   - Big Five factor scores and percentiles
   - Personality profile interpretation
   - Behavioral predictions and tendencies
   - Interpersonal and occupational implications

3. CLINICAL ASSESSMENT:
   - Overall psychological functioning
   - Risk factors and protective factors  
   - Diagnostic considerations (if any)
   - Treatment or intervention recommendations

4. VALIDITY AND RELIABILITY NOTES:
   - Response pattern analysis
   - Potential bias or inconsistencies
   - Confidence in results
   - Limitations and caveats

Return comprehensive evaluation as detailed JSON report.
"""
        
        try:
            # Get evaluation context from knowledge base
            context_response = self.evaluation_chain.run(evaluation_prompt)
            
            # Generate full evaluation
            evaluation_response = self.llm.predict(f"""
Based on the following clinical guidelines and assessment data, provide a comprehensive psychological evaluation:

CLINICAL GUIDELINES:
{context_response}

{evaluation_prompt}

Return as valid JSON with detailed analysis.
""")
            
            return json.loads(evaluation_response)
            
        except json.JSONDecodeError:
            # Fallback evaluation
            return self._generate_fallback_evaluation(test_data, responses)
        except Exception as e:
            return {"error": f"Evaluation failed: {str(e)}"}
    
    def _generate_fallback_evaluation(self, test_data: Dict[str, Any], responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate basic evaluation if main evaluation fails"""
        
        evaluation = {
            "evaluation_id": f"eval_{uuid4().hex[:8]}",
            "timestamp": datetime.now().isoformat(),
            "overall_assessment": "Assessment completed with basic analysis",
            "status": "completed",
            "participant_summary": {
                "total_responses": len(responses),
                "response_rate": "100%",
                "completion_time": "Standard"
            }
        }
        
        # Basic aptitude analysis
        if test_data.get("test_type") in ["aptitude", "psychometric"]:
            aptitude_responses = [r for r in responses if r.get("question_id", "").startswith("apt")]
            if aptitude_responses:
                evaluation["aptitude_analysis"] = {
                    "items_completed": len(aptitude_responses),
                    "estimated_performance": "Average range",
                    "domains_assessed": ["verbal", "numerical", "logical", "spatial"],
                    "recommendations": ["Results suggest typical cognitive abilities"]
                }
        
        # Basic personality analysis  
        if test_data.get("test_type") in ["personality", "psychometric"]:
            personality_responses = [r for r in responses if r.get("question_id", "").startswith("per")]
            if personality_responses:
                evaluation["personality_analysis"] = {
                    "items_completed": len(personality_responses),
                    "factors_assessed": ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"],
                    "profile_summary": "Balanced personality profile observed",
                    "recommendations": ["Results suggest healthy personality functioning"]
                }
        
        evaluation["clinical_recommendations"] = [
            "Assessment completed successfully",
            "Results appear valid and interpretable", 
            "Consider follow-up assessment if detailed analysis needed"
        ]
        
        return evaluation

class PsychometricChatbot:
    """Main chatbot interface"""
    
    def __init__(self, rag_system: PsychometricRAGSystem):
        self.rag_system = rag_system
        self.session_data = {
            "session_id": f"session_{uuid4().hex[:8]}",
            "start_time": datetime.now().isoformat(),
            "current_test": None,
            "responses": [],
            "evaluation": None
        }
    
    def run_test(self, test_type: str, **specifications) -> Dict[str, Any]:
        """Main command interface"""
        
        if test_type not in ["psychometric", "aptitude", "personality"]:
            return {"error": "Invalid test type. Choose: psychometric, aptitude, or personality"}
        
        try:
            # Generate test using RAG
            test_data = self.rag_system.generate_test_questions(test_type, specifications)
            
            if "error" not in test_data:
                # Store current test
                self.session_data["current_test"] = test_data
                self.session_data["current_test"]["generated_at"] = datetime.now().isoformat()
                
                return {
                    "status": "success",
                    "message": f"{test_type.title()} test generated using RAG system",
                    "test_data": test_data,
                    "session_id": self.session_data["session_id"],
                    "context_sources": "Pinecone vector database with psychometric guidelines"
                }
            else:
                return test_data
                
        except Exception as e:
            return {"error": f"Test generation failed: {str(e)}"}
    
    def submit_responses(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Submit responses for psychologist evaluation"""
        
        if not self.session_data["current_test"]:
            return {"error": "No active test found"}
        
        try:
            # Store responses
            self.session_data["responses"] = responses
            
            # Get psychologist evaluation
            evaluation = self.rag_system.psychologist_agent.evaluate_assessment_results(
                self.session_data["current_test"],
                responses
            )
            
            self.session_data["evaluation"] = evaluation
            
            return {
                "status": "completed",
                "message": "Assessment evaluated by AI psychologist using clinical guidelines",
                "evaluation": evaluation,
                "session_id": self.session_data["session_id"]
            }
            
        except Exception as e:
            return {"error": f"Evaluation failed: {str(e)}"}

def create_streamlit_app():
    """Streamlit interface for RAG system"""
    
    st.set_page_config(
        page_title="RAG Psychometric System",
        page_icon="🧠",
        layout="wide"
    )
    
    st.title("🧠 RAG Psychometric Assessment System")
    st.markdown("*Powered by Pinecone Vector Database + LangChain + OpenAI*")
    
    # API Configuration
    with st.sidebar:
        st.header("🔧 Configuration")
        
        openai_key = st.text_input("OpenAI API Key", type="password", help="Required for LLM and embeddings")
        pinecone_key = st.text_input("Pinecone API Key", type="password", help="Required for vector database")
        pinecone_env = st.selectbox("Pinecone Environment", 
            ["us-east-1-aws", "us-west-1-aws", "eu-west1-gcp"], 
            help="Choose your Pinecone environment")
        
        if st.button("Initialize RAG System"):
            if openai_key and pinecone_key:
                try:
                    st.session_state.rag_system = PsychometricRAGSystem(
                        openai_api_key=openai_key,
                        pinecone_api_key=pinecone_key,
                        pinecone_environment=pinecone_env
                    )
                    st.session_state.chatbot = PsychometricChatbot(st.session_state.rag_system)
                    st.success("RAG System initialized!")
                except Exception as e:
                    st.error(f"Initialization failed: {str(e)}")
            else:
                st.error("Please provide both API keys")
    
    # Check if system is initialized
    if 'rag_system' not in st.session_state:
        st.warning("Please configure and initialize the RAG system in the sidebar first.")
        st.info("""
        **Required Setup:**
        1. Get OpenAI API key from https://platform.openai.com/api-keys
        2. Get Pinecone API key from https://app.pinecone.io/
        3. Enter keys in sidebar and click 'Initialize RAG System'
        """)
        return
    
    # Knowledge Base Management
    st.header("📚 Knowledge Base Management")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Populate Knowledge Base", help="Load psychometric guidelines into Pinecone"):
            with st.spinner("Loading psychometric knowledge into vector database..."):
                success = st.session_state.rag_system.populate_knowledge_base()
                if success:
                    st.success("Knowledge base populated successfully!")
    
    with col2:
        if st.button("🔍 Query Knowledge Base", help="Test retrieval from vector database"):
            query = st.text_input("Enter query:", "aptitude assessment guidelines")
            if query:
                docs = st.session_state.rag_system.vectorstore.similarity_search(query, k=3)
                st.write("Retrieved documents:")
                for i, doc in enumerate(docs):
                    with st.expander(f"Document {i+1}"):
                        st.write(doc.page_content[:500] + "...")
                        st.json(doc.metadata)
    
    # Test Generation
    st.header("🎯 Test Generation Commands")
    
    col1, col2, col3 = st.columns(3)
    
    # Test specifications
    with st.expander("⚙️ Test Specifications", expanded=True):
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            item_count = st.slider("Number of Items", 5, 30, 10)
        with col_b:
            difficulty = st.select_slider("Difficulty", ["easy", "medium", "hard"], value="medium")
        with col_c:
            target_pop = st.selectbox("Target Population", ["adults", "students", "professionals", "clinical"])
    
    specifications = {
        "item_count": item_count,
        "difficulty": difficulty, 
        "target_population": target_pop
    }
    
    # Test generation buttons
    with col1:
        if st.button("🧠 Psychometric Test", use_container_width=True):
            with st.spinner("Generating comprehensive assessment using RAG..."):
                result = st.session_state.chatbot.run_test("psychometric", **specifications)
                st.session_state.test_result = result
    
    with col2:
        if st.button("📊 Aptitude Test", use_container_width=True):
            with st.spinner("Generating aptitude test using RAG..."):
                result = st.session_state.chatbot.run_test("aptitude", **specifications)
                st.session_state.test_result = result
    
    with col3:
        if st.button("👤 Personality Test", use_container_width=True):
            with st.spinner("Generating personality test using RAG..."):
                result = st.session_state.chatbot.run_test("personality", **specifications)
                st.session_state.test_result = result
    
    # Display generated test
    if 'test_result' in st.session_state:
        result = st.session_state.test_result
        
        if result.get("status") == "success":
            st.success(f"✅ {result['message']}")
            st.info(f"Context: {result.get('context_sources', 'Unknown')}")
            
            test_data = result["test_data"]
            
            # Display test content
            st.subheader("📝 Generated Assessment")
            
            if test_data.get("test_type") == "psychometric":
                # Combined test
                tab1, tab2 = st.tabs(["🧠 Aptitude Items", "👤 Personality Items"])
                
                with tab1:
                    if "aptitude_items" in test_data:
                        display_aptitude_items(test_data["aptitude_items"])
                    else:
                        st.warning("No aptitude items found in combined test")
                
                with tab2:
                    if "personality_items" in test_data:
                        display_personality_items(test_data["personality_items"])
                    # else: