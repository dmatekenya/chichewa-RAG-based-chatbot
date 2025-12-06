"""
RAG Chain Module

This module integrates translation, document retrieval, and LLM to create
a complete Chichewa-English RAG chatbot with smart query handling.
"""

from typing import Dict, List, Optional, Tuple
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.translator import Translator
from src.document_processor import DocumentProcessor

# Load environment variables
load_dotenv()


class ChichewaRAGChain:
    """RAG-based chatbot that answers in Chichewa using English documents"""
    
    def __init__(
        self,
        model: str = "gpt-4",
        temperature: float = 0.7,
        retrieval_k: int = 5  # Increased from 3 to 5 for better coverage
    ):
        """
        Initialize the RAG chain
        
        Args:
            model: OpenAI model for answer generation
            temperature: Temperature for answer generation (0.0-1.0)
            retrieval_k: Number of document chunks to retrieve
        """
        self.model = model
        self.temperature = temperature
        self.retrieval_k = retrieval_k
        
        # Initialize components
        self.translator = Translator(model="gpt-4", temperature=0.3)
        self.doc_processor = DocumentProcessor()
        
        # Load or create vector store
        try:
            self.vectorstore = self.doc_processor.load_vectorstore()
        except FileNotFoundError:
            # Vector store doesn't exist - create it
            print("Vector store not found. Creating from documents...")
            self.vectorstore = self.doc_processor.process_documents(force_recreate=True)
        
        # Initialize LLM for answer generation
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Initialize query classifier
        self.classifier_llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.0,  # Low temperature for consistent classification
            api_key=os.getenv("OPENAI_API_KEY")
        )
    
    def classify_query(self, english_query: str) -> str:
        """
        Classify the user's query intent with enhanced categories
        
        Args:
            english_query: Query in English
            
        Returns:
            Classification: greeting, out_of_scope, product_inquiry, comparison_query, 
                          procedure_question, or general_info
        """
        classification_prompt = """You are a query classifier for a bank products chatbot.

Classify the following query into ONE of these categories:
- "greeting": Greetings, hello, how are you, thank you, goodbye
- "out_of_scope": Weather, math, current events, personal advice, non-banking topics
- "product_inquiry": Questions about specific bank products (accounts, loans, cards, services)
- "comparison_query": Comparing multiple products or asking about differences
- "procedure_question": How to open account, apply for loan, use service, requirements
- "general_info": General banking information, fees, rates, terms

Query: {query}

Respond with ONLY ONE WORD from the categories above."""

        messages = [
            HumanMessage(content=classification_prompt.format(query=english_query))
        ]
        
        try:
            response = self.classifier_llm.invoke(messages)
            classification = response.content.strip().lower()
            
            # Validate classification
            valid_categories = [
                "greeting", "out_of_scope", "product_inquiry", 
                "comparison_query", "procedure_question", "general_info"
            ]
            
            if classification not in valid_categories:
                # Default to product_inquiry if unclear
                return "product_inquiry"
            
            return classification
        
        except Exception as e:
            print(f"Classification error: {e}")
            return "product_inquiry"  # Default to product inquiry on error
    
    def handle_greeting(self, language: str = "chichewa") -> str:
        """
        Generate a friendly greeting response
        
        Args:
            language: Response language ("english" or "chichewa")
            
        Returns:
            Greeting message in specified language
        """
        greeting_english = (
            "Hello! I'm here to help you with questions about bank products and services. "
            "You can ask me about different types of accounts, loans, cards, payments, "
            "or any banking services. What would you like to know?"
        )
        
        if language == "english":
            return greeting_english
        else:
            greeting_chichewa = self.translator.translate_to_chichewa(greeting_english)
            return greeting_chichewa
    
    def handle_out_of_scope(self, language: str = "chichewa") -> str:
        """
        Handle out-of-scope queries gracefully
        
        Args:
            language: Response language ("english" or "chichewa")
            
        Returns:
            Polite response in specified language
        """
        out_of_scope_english = (
            "I'm sorry, but I'm designed specifically to answer questions about bank products "
            "and services. I can help you with information about accounts, loans, cards, "
            "payment services, and other banking topics. "
            "Is there anything about our bank products you'd like to know?"
        )
        
        if language == "english":
            return out_of_scope_english
        else:
            out_of_scope_chichewa = self.translator.translate_to_chichewa(out_of_scope_english)
            return out_of_scope_chichewa
    
    def retrieve_documents(self, english_query: str) -> List[Dict]:
        """
        Retrieve relevant document chunks
        
        Args:
            english_query: Query in English
            
        Returns:
            List of relevant documents with metadata
        """
        try:
            docs = self.vectorstore.similarity_search(
                english_query,
                k=self.retrieval_k
            )
            
            # Format documents with metadata
            retrieved_docs = []
            for doc in docs:
                retrieved_docs.append({
                    "content": doc.page_content,
                    "source": doc.metadata.get("source", "Unknown"),
                    "file_path": doc.metadata.get("file_path", "")
                })
            
            return retrieved_docs
        
        except Exception as e:
            print(f"Document retrieval error: {e}")
            return []
    
    def generate_answer(
        self,
        english_query: str,
        retrieved_docs: List[Dict],
        language: str = "english"
    ) -> Tuple[str, List[str]]:
        """
        Generate a natural, helpful answer based on retrieved documents
        
        Args:
            english_query: Query in English
            retrieved_docs: List of retrieved document chunks
            language: Target language for response tone
            
        Returns:
            Tuple of (answer in English, list of source documents)
        """
        if not retrieved_docs:
            # Generate helpful "no results" message
            no_results_prompt = f"""You are a friendly, helpful bank assistant. A customer asked: "{english_query}"

Unfortunately, you couldn't find specific information in your knowledge base to answer this question.

Write a warm, helpful response that:
1. Acknowledges their question politely
2. Apologizes for not having that specific information
3. Suggests they try rephrasing the question or asking about related topics
4. Offers to help with other banking questions
5. Keeps a friendly, conversational tone

Response:"""
            
            messages = [HumanMessage(content=no_results_prompt)]
            
            try:
                response = self.llm.invoke(messages)
                return response.content.strip(), []
            except Exception as e:
                print(f"Error generating no-results message: {e}")
                return "I apologize, but I couldn't find specific information about that in my knowledge base. Could you try rephrasing your question or asking about a different aspect of our banking products?", []
        
        # Prepare context from retrieved documents
        context_parts = []
        sources = []
        
        for i, doc in enumerate(retrieved_docs, 1):
            context_parts.append(f"[Document {i} - {doc['source']}]\n{doc['content']}")
            if doc['source'] not in sources:
                sources.append(doc['source'])
        
        context = "\n\n".join(context_parts)
        
        # Create prompt for answer generation with natural, conversational tone
        answer_prompt = f"""You are a friendly, knowledgeable bank assistant helping customers understand banking products and services.

Context from our product documentation:
{context}

Customer's Question: {english_query}

Instructions:
- Provide a warm, conversational answer based on the context
- Be specific and include relevant details from the documents
- Use a friendly, helpful tone (not robotic or overly formal)
- If information is incomplete, acknowledge what you know and what you don't
- Format the answer clearly with bullet points or paragraphs as appropriate
- End with an offer to help further if needed

Answer:"""

        messages = [
            HumanMessage(content=answer_prompt)
        ]
        
        try:
            response = self.llm.invoke(messages)
            answer = response.content.strip()
            return answer, sources
        
        except Exception as e:
            print(f"Answer generation error: {e}")
            return "I encountered an error generating the answer.", sources
    
    def answer_query(
        self,
        user_query: str,
        return_metadata: bool = False
    ) -> Dict:
        """
        Complete RAG pipeline with language detection and intent-based routing
        
        Args:
            user_query: User's query in English or Chichewa
            return_metadata: If True, return additional metadata
            
        Returns:
            Dictionary with answer and optional metadata
        """
        print(f"\n🔍 Processing query: {user_query}")
        
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
            print("   [2] Query already in English, skipping translation")
            english_query = user_query
        
        # Step 3: Classify query intent
        print("   [3] Classifying query intent...")
        query_type = self.classify_query(english_query)
        print(f"   → Intent: {query_type}")
        
        # Step 4: Handle based on classification
        if query_type == "greeting":
            print("   [4] Handling as greeting")
            answer = self.handle_greeting(language=detected_language)
            
            return {
                "answer": answer,
                "query_type": "greeting",
                "sources": [],
                "english_query": english_query,
                "detected_language": detected_language
            }
        
        elif query_type == "out_of_scope":
            print("   [4] Handling as out-of-scope")
            answer = self.handle_out_of_scope(language=detected_language)
            
            return {
                "answer": answer,
                "query_type": "out_of_scope",
                "sources": [],
                "english_query": english_query,
                "detected_language": detected_language
            }
        
        else:  # product inquiry, comparison, procedure, or general info
            # Step 4: Retrieve relevant documents
            print("   [4] Retrieving relevant documents...")
            retrieved_docs = self.retrieve_documents(english_query)
            print(f"   → Retrieved {len(retrieved_docs)} documents")
            
            # Step 5: Generate answer in English
            print("   [5] Generating answer...")
            english_answer, sources = self.generate_answer(
                english_query, 
                retrieved_docs, 
                language=detected_language
            )
            print(f"   → English answer: {english_answer[:100]}...")
            
            # Step 6: Translate answer if needed
            if detected_language == "chichewa":
                print("   [6] Translating answer to Chichewa...")
                final_answer = self.translator.translate_to_chichewa(english_answer)
            else:
                print("   [6] Keeping answer in English")
                final_answer = english_answer
            
            result = {
                "answer": final_answer,
                "query_type": query_type,
                "sources": sources,
                "english_query": english_query,
                "detected_language": detected_language
            }
            
            if return_metadata:
                result.update({
                    "english_answer": english_answer,
                    "retrieved_docs": retrieved_docs
                })
            
            return result


if __name__ == "__main__":
    # Test the RAG chain
    print("=" * 70)
    print("Testing Bank Products Chatbot with Enhanced Classification")
    print("=" * 70)
    
    # Initialize the RAG chain
    rag_chain = ChichewaRAGChain()
    
    # Test queries in both English and Chichewa
    test_queries = [
        # English greeting
        ("Hello, how are you?", "English"),
        
        # Chichewa greeting
        ("Moni, muli bwanji?", "Chichewa"),
        
        # English out of scope
        ("What's the weather like today?", "English"),
        
        # Chichewa out of scope
        ("Kwacha bwanji lero?", "Chichewa"),
        
        # English product inquiry
        ("What types of savings accounts do you have?", "English"),
        
        # Chichewa product inquiry
        ("Kodi muli ndi ma akaunti a mtundu wanji?", "Chichewa"),
        
        # English comparison query
        ("What's the difference between a current account and savings account?", "English"),
        
        # Chichewa loan inquiry
        ("Ndiuzeni za mortgage loan", "Chichewa"),
        
        # English procedure question
        ("How do I open a savings account?", "English"),
    ]
    
    for query, expected_lang in test_queries:
        print("\n" + "=" * 70)
        result = rag_chain.answer_query(query, return_metadata=False)
        
        print(f"\n📥 Query ({expected_lang}): {query}")
        print(f"🌍 Detected Language:    {result['detected_language']}")
        print(f"🔍 Intent:               {result['query_type']}")
        print(f"📤 Answer:               {result['answer'][:150]}...")
        
        if result['sources']:
            print(f"📚 Sources:              {', '.join(result['sources'][:3])}")
    
    print("\n" + "=" * 70)
    print("Testing complete!")
    print("=" * 70)
