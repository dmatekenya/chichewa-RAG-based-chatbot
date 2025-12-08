"""
Structured Prompt Engineering (SPE) Chain

Alternative to RAG for small knowledge bases with low-resource languages.
Encodes entire knowledge base in structured prompts instead of vector retrieval.

Approach:
- Load all banking product data into structured format
- Encode in prompt as JSON/tables
- Use GPT-4's large context window
- Direct generation without retrieval step

Advantages for low-resource scenarios:
- No embedding quality issues
- No retrieval errors
- Full context always available
- Better for small knowledge bases (<50 documents)
"""

from typing import Dict, List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.translator import Translator
from src.chichewa_phrases import build_chichewa_generation_guidelines

# Load environment variables
load_dotenv()


class StructuredPromptChain:
    """
    Structured Prompt Engineering approach for multilingual banking chatbot.
    
    Uses full knowledge base in prompt instead of RAG retrieval.
    Ideal for small knowledge bases with low-resource target languages.
    """
    
    def __init__(
        self,
        model: str = "gpt-4",
        temperature: float = 0.7,
        knowledge_base_path: str = "data/knowledge_base.json"
    ):
        """
        Initialize SPE chain with structured knowledge base.
        
        Args:
            model: OpenAI model
            temperature: Generation temperature
            knowledge_base_path: Path to structured knowledge base JSON
        """
        self.model = model
        self.temperature = temperature
        
        # Initialize components
        self.translator = Translator(model="gpt-4", temperature=0.3)
        
        # Load structured knowledge base
        self.knowledge_base = self._load_or_create_knowledge_base(knowledge_base_path)
        
        # Initialize LLMs
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.classifier_llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.0,
            api_key=os.getenv("OPENAI_API_KEY")
        )
    
    def _load_or_create_knowledge_base(self, path: str) -> Dict:
        """
        Load structured knowledge base or create from documents.
        
        For now, returns a structured template. In production, this would
        parse PDFs into structured JSON.
        
        Args:
            path: Path to knowledge base JSON
            
        Returns:
            Structured knowledge base dictionary
        """
        # TODO: Parse actual PDFs into this structure
        # For now, using example structure
        
        return {
            "products": {
                "amayi_angathe": {
                    "name": "Amayi Angathe Business Savings Account",
                    "category": "savings",
                    "target_audience": "Women entrepreneurs and business owners",
                    "benefits": [
                        "Free monthly maintenance for the first 6 months",
                        "Free ATM card upon account opening",
                        "Low minimum balance of MK 3,000",
                        "Free salary payments via EFT",
                        "50% discount on EFT transaction fees",
                        "Access to Mo626 services without charges"
                    ],
                    "requirements": [
                        "Valid national ID",
                        "Proof of business registration or trading license",
                        "Initial deposit of MK 3,000",
                        "Passport-sized photograph",
                        "Proof of residence"
                    ],
                    "fees": {
                        "monthly_maintenance": "MK 0 (first 6 months), then MK 200",
                        "atm_withdrawals": "Free at FDH ATMs, MK 150 at other banks",
                        "balance_inquiry": "Free",
                        "eft_transfers": "50% discount on standard fees"
                    },
                    "features": [
                        "Mobile banking access",
                        "Internet banking",
                        "ATM/debit card",
                        "Overdraft facility available",
                        "Cheque book available"
                    ]
                },
                "mlimi": {
                    "name": "Mlimi Loan",
                    "category": "loan",
                    "target_audience": "Farmers and agricultural businesses",
                    "benefits": [
                        "Competitive interest rates for agriculture",
                        "Flexible repayment schedule aligned with harvest cycles",
                        "Quick loan processing (7-10 days)",
                        "Loan amounts from MK 50,000 to MK 5,000,000",
                        "No collateral required for loans under MK 200,000"
                    ],
                    "requirements": [
                        "Valid national ID",
                        "Proof of farming activity (land ownership/lease)",
                        "Business plan or farming proposal",
                        "Collateral for loans above MK 200,000",
                        "Bank account with FDH for at least 3 months"
                    ],
                    "fees": {
                        "interest_rate": "18-22% per annum (depending on loan size)",
                        "processing_fee": "2% of loan amount",
                        "insurance": "1.5% of loan amount annually"
                    },
                    "features": [
                        "Grace period available during planting season",
                        "Flexible repayment terms (6-24 months)",
                        "Loan top-up facility for existing customers",
                        "Agricultural insurance options"
                    ]
                }
            },
            "general_info": {
                "bank_name": "FDH Bank",
                "working_hours": "Monday-Friday: 8:00 AM - 5:00 PM, Saturday: 8:00 AM - 12:00 PM",
                "customer_service": "Call 313 or +265 1 832 777",
                "website": "www.fdhbank.com"
            }
        }
    
    def classify_query(self, english_query: str) -> str:
        """
        Classify query type (same as RAG chain).
        
        Args:
            english_query: Query in English
            
        Returns:
            Classification type
        """
        classification_prompt = """You are a query classifier for a bank products chatbot.

Classify the following query into ONE of these categories:
- "greeting": Greetings, hello, how are you, thank you, goodbye
- "out_of_scope": Weather, math, current events, personal advice, non-banking topics
- "product_inquiry": Questions about specific bank products (accounts, loans, cards, services)
- "comparison_query": Comparing multiple products or asking about differences
- "procedure_question": How to open account, apply for loan, use service, requirements
- "contact_inquiry": Phone numbers, email addresses, branch locations, contact information
- "general_info": General banking information, fees, rates, terms

Query: {query}

Respond with ONLY ONE WORD from the categories above."""

        messages = [
            HumanMessage(content=classification_prompt.format(query=english_query))
        ]
        
        try:
            response = self.classifier_llm.invoke(messages)
            classification = response.content.strip().lower()
            
            valid_categories = [
                "greeting", "out_of_scope", "product_inquiry", 
                "comparison_query", "procedure_question", "general_info",
                "contact_inquiry"
            ]
            
            if classification not in valid_categories:
                return "product_inquiry"
            
            return classification
        
        except Exception as e:
            print(f"Classification error: {e}")
            return "product_inquiry"
    
    def detect_query_intent(self, english_query: str) -> str:
        """
        Detect specific aspect being asked about.
        
        Args:
            english_query: Query in English
            
        Returns:
            Intent: benefits/requirements/fees/features/general
        """
        query_lower = english_query.lower()
        
        if any(word in query_lower for word in ['benefit', 'advantage', 'ubwino', 'why choose', 'what do i get']):
            return 'benefits'
        elif any(word in query_lower for word in ['requirement', 'eligibility', 'zofunikira', 'qualify', 'need to', 'criteria']):
            return 'requirements'
        elif any(word in query_lower for word in ['fee', 'cost', 'charge', 'price', 'mtengo', 'phindu', 'interest rate', 'how much']):
            return 'fees'
        elif any(word in query_lower for word in ['how does', 'how to use', 'functionality', 'works', 'feature']):
            return 'features'
        else:
            return 'general'
    
    def extract_product_from_query(self, english_query: str) -> Optional[str]:
        """
        Extract product name from query.
        
        Args:
            english_query: Query in English
            
        Returns:
            Product key if found, else None
        """
        query_lower = english_query.lower()
        
        # Map product mentions to keys
        product_mappings = {
            'amayi angathe': 'amayi_angathe',
            'amayi': 'amayi_angathe',
            'mlimi': 'mlimi',
            'farmer': 'mlimi',
            'agricultural': 'mlimi'
        }
        
        for mention, key in product_mappings.items():
            if mention in query_lower:
                return key
        
        return None
    
    def build_structured_context(
        self,
        query_intent: str,
        product_key: Optional[str] = None
    ) -> str:
        """
        Build structured context from knowledge base based on intent.
        
        Args:
            query_intent: Detected intent (benefits/requirements/fees/features/general)
            product_key: Specific product key if identified
            
        Returns:
            Formatted context string
        """
        if product_key and product_key in self.knowledge_base['products']:
            # Specific product context
            product = self.knowledge_base['products'][product_key]
            
            context = f"PRODUCT: {product['name']}\n"
            context += f"CATEGORY: {product['category']}\n"
            context += f"TARGET AUDIENCE: {product['target_audience']}\n\n"
            
            # Add intent-specific sections
            if query_intent == 'benefits' or query_intent == 'general':
                context += "BENEFITS:\n"
                for i, benefit in enumerate(product['benefits'], 1):
                    context += f"{i}. {benefit}\n"
                context += "\n"
            
            if query_intent == 'requirements' or query_intent == 'general':
                context += "REQUIREMENTS:\n"
                for i, req in enumerate(product['requirements'], 1):
                    context += f"{i}. {req}\n"
                context += "\n"
            
            if query_intent == 'fees' or query_intent == 'general':
                context += "FEES:\n"
                for fee_type, amount in product['fees'].items():
                    context += f"- {fee_type.replace('_', ' ').title()}: {amount}\n"
                context += "\n"
            
            if query_intent == 'features' or query_intent == 'general':
                context += "FEATURES:\n"
                for i, feature in enumerate(product['features'], 1):
                    context += f"{i}. {feature}\n"
                context += "\n"
        
        else:
            # General context - all products
            context = "AVAILABLE BANKING PRODUCTS:\n\n"
            
            for key, product in self.knowledge_base['products'].items():
                context += f"• {product['name']} ({product['category']})\n"
                context += f"  Target: {product['target_audience']}\n"
                if query_intent in ['benefits', 'general']:
                    context += f"  Key Benefits: {', '.join(product['benefits'][:3])}\n"
                context += "\n"
        
        return context
    
    def generate_answer(
        self,
        english_query: str,
        structured_context: str,
        target_language: str = "chichewa",
        query_intent: str = "general"
    ) -> str:
        """
        Generate answer using structured prompt engineering.
        
        Args:
            english_query: Query in English
            structured_context: Structured knowledge base context
            target_language: Target language for response
            query_intent: Detected query intent
            
        Returns:
            Answer in target language
        """
        # Build intent-specific instructions
        intent_instructions = {
            'benefits': "Focus ONLY on benefits and advantages. Do NOT discuss requirements or fees unless specifically asked.",
            'requirements': "Focus ONLY on requirements and eligibility criteria. Do NOT discuss benefits.",
            'fees': "Focus ONLY on fees, costs, and charges. Be specific about amounts.",
            'features': "Focus on how the product works and its features.",
            'general': "Provide a balanced overview covering key aspects."
        }
        
        intent_instruction = intent_instructions.get(query_intent, intent_instructions['general'])
        
        if target_language == "chichewa":
            guidelines = build_chichewa_generation_guidelines()
            
            prompt = f"""Ndinu wothandiza wa banki yomwe ikuthandiza maklienti kudziwa zambiri za zinthu za banki.

ZAMBIRI ZA ZINTHU ZA BANKI (Structured Knowledge Base):
{structured_context}

FUNSO LA MUNTHU (mu Chingerezi): {english_query}

MALANGIZO A NKHANI:
{intent_instruction}

{guidelines}

MALANGIZO OFUNIKIRA:
- Yankhani m'CHICHEWA CHOYAMBA chachilengedwe (osati kumasulira mawu ndi mawu)
- Gwiritsani ntchito zambiri zomwe zaperekedwa pamwambapa
- Sungani mawu a banking mu Chingerezi (account, loan, ATM, MK, EFT, etc.)
- Khalani ochezera, wothandiza, ndi woyamba
- Gwiritsani ntchito mawu olumikizana a Chichichewa (komanso, zomwe, moti, motsatira, chifukwa, etc.)
- Konzani yankho bwino ndi ma bullet points ngati pali zambiri
- Maliza ndi kupereka thandizo

YANKHANI M'CHICHEWA (osati kumasulira, koma kulemba mwachibadwa):"""
        
        else:
            prompt = f"""You are a friendly, knowledgeable bank assistant helping customers understand banking products and services.

STRUCTURED KNOWLEDGE BASE:
{structured_context}

Customer's Question: {english_query}

FOCUS INSTRUCTION:
{intent_instruction}

Instructions:
- Provide a warm, conversational answer based on the structured information above
- Be specific and include relevant details
- Use a friendly, helpful tone (not robotic or overly formal)
- Format the answer clearly with bullet points or paragraphs as appropriate
- End with an offer to help further if needed

Answer:"""
        
        messages = [HumanMessage(content=prompt)]
        
        try:
            response = self.llm.invoke(messages)
            return response.content.strip()
        
        except Exception as e:
            print(f"Generation error: {e}")
            if target_language == "chichewa":
                return "Pepani, panali vuto pakupanga yankho. Mungafunse mwanjira ina?"
            else:
                return "I apologize, there was an error generating the answer. Could you try rephrasing your question?"
    
    def answer_query(self, user_query: str) -> Dict:
        """
        Complete SPE pipeline: classify → detect intent → build context → generate.
        
        Args:
            user_query: User's query in English or Chichewa
            
        Returns:
            Dictionary with answer and metadata
        """
        print(f"\n🔍 [SPE] Processing query: {user_query}")
        
        # Step 1: Detect language
        print("   [1] Detecting language...")
        detected_language = self.translator.detect_language(user_query)
        print(f"   → Language: {detected_language}")
        
        # Step 2: Translate to English if needed
        if detected_language == "chichewa":
            print("   [2] Translating to English...")
            english_query = self.translator.translate_to_english(user_query)
            print(f"   → English query: {english_query}")
        else:
            print("   [2] Query already in English")
            english_query = user_query
        
        # Step 3: Classify query type
        print("   [3] Classifying query type...")
        query_type = self.classify_query(english_query)
        print(f"   → Query type: {query_type}")
        
        # Step 4: Detect query intent
        print("   [4] Detecting query intent...")
        query_intent = self.detect_query_intent(english_query)
        print(f"   → Query intent: {query_intent}")
        
        # Step 5: Extract product from query
        print("   [5] Extracting product...")
        product_key = self.extract_product_from_query(english_query)
        print(f"   → Product: {product_key or 'general'}")
        
        # Step 6: Build structured context
        print("   [6] Building structured context...")
        structured_context = self.build_structured_context(query_intent, product_key)
        print(f"   → Context size: {len(structured_context)} characters")
        
        # Step 7: Generate answer
        print(f"   [7] Generating answer in {detected_language}...")
        answer = self.generate_answer(
            english_query,
            structured_context,
            target_language=detected_language,
            query_intent=query_intent
        )
        print(f"   → Answer: {answer[:100]}...")
        
        return {
            "answer": answer,
            "query_type": query_type,
            "query_intent": query_intent,
            "product": product_key,
            "english_query": english_query,
            "detected_language": detected_language,
            "approach": "structured_prompt_engineering"
        }


if __name__ == "__main__":
    # Test SPE chain
    print("=" * 70)
    print("Testing Structured Prompt Engineering Approach")
    print("=" * 70)
    
    spe_chain = StructuredPromptChain()
    
    test_queries = [
        "Ubwino wa amayi angathe account",
        "Zofunikira za mlimi loan",
        "Mtengo wa amayi angathe account",
        "What are the benefits of the Amayi Angathe account?"
    ]
    
    for query in test_queries:
        print("\n" + "=" * 70)
        result = spe_chain.answer_query(query)
        print(f"\n📥 Query: {query}")
        print(f"📤 Answer: {result['answer'][:200]}...")
        print(f"🎯 Intent: {result['query_intent']}, Product: {result['product']}")
    
    print("\n" + "=" * 70)
