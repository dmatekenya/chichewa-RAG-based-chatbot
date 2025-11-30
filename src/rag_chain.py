"""
RAG Chain Module

This module integrates translation, document retrieval, and LLM to create
a complete Chichewa-English RAG chatbot with smart query handling.
"""

from typing import Dict, List, Optional, Tuple
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate
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
        retrieval_k: int = 3
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
        
        # Load vector store
        self.vectorstore = self.doc_processor.load_vectorstore()
        
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
        Classify the user's query type
        
        Args:
            english_query: Query in English
            
        Returns:
            Classification: "greeting", "out_of_scope", or "relevant"
        """
        classification_prompt = """You are a query classifier for a chatbot that answers questions about news articles.

Classify the following query into ONE of these categories:
- "greeting": If it's a greeting, hello, how are you, etc.
- "out_of_scope": If it's about weather, math, current events outside the documents, personal advice, etc.
- "relevant": If it's asking about news, events, people, or information that could be in news articles

Query: {query}

Respond with ONLY ONE WORD: greeting, out_of_scope, or relevant"""

        messages = [
            HumanMessage(content=classification_prompt.format(query=english_query))
        ]
        
        try:
            response = self.classifier_llm.invoke(messages)
            classification = response.content.strip().lower()
            
            # Validate classification
            if classification not in ["greeting", "out_of_scope", "relevant"]:
                # Default to relevant if unclear
                return "relevant"
            
            return classification
        
        except Exception as e:
            print(f"Classification error: {e}")
            return "relevant"  # Default to relevant on error
    
    def handle_greeting(self) -> str:
        """
        Generate a friendly greeting response in Chichewa
        
        Returns:
            Greeting message in Chichewa
        """
        greeting_english = (
            "Hello! I'm here to help you with questions about news articles. "
            "You can ask me about events, people, sports, politics, or any news topics. "
            "What would you like to know?"
        )
        
        greeting_chichewa = self.translator.translate_to_chichewa(greeting_english)
        return greeting_chichewa
    
    def handle_out_of_scope(self, original_query_chichewa: str) -> str:
        """
        Handle out-of-scope queries gracefully
        
        Args:
            original_query_chichewa: Original query in Chichewa
            
        Returns:
            Polite response in Chichewa
        """
        out_of_scope_english = (
            "I'm sorry, but I'm designed specifically to answer questions about news articles "
            "in my knowledge base. I can help you with information about events, people, sports, "
            "politics, and other news topics covered in the articles. "
            "Is there anything about the news you'd like to know?"
        )
        
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
        retrieved_docs: List[Dict]
    ) -> Tuple[str, List[str]]:
        """
        Generate an answer based on retrieved documents
        
        Args:
            english_query: Query in English
            retrieved_docs: List of retrieved document chunks
            
        Returns:
            Tuple of (answer in English, list of source documents)
        """
        if not retrieved_docs:
            return "I couldn't find any relevant information in the documents.", []
        
        # Prepare context from retrieved documents
        context_parts = []
        sources = []
        
        for i, doc in enumerate(retrieved_docs, 1):
            context_parts.append(f"[Document {i} - {doc['source']}]\n{doc['content']}")
            if doc['source'] not in sources:
                sources.append(doc['source'])
        
        context = "\n\n".join(context_parts)
        
        # Create prompt for answer generation
        answer_prompt = f"""You are a helpful assistant answering questions based on news articles.

Use the following context from news articles to answer the question. If the answer cannot be found in the context, say so clearly.

Context:
{context}

Question: {english_query}

Provide a clear, accurate answer based on the context above. If the information is not in the context, say "I don't have information about that in the available articles." """

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
        chichewa_query: str,
        return_metadata: bool = False
    ) -> Dict:
        """
        Complete RAG pipeline: translate query, classify, retrieve, generate, translate back
        
        Args:
            chichewa_query: User's query in Chichewa
            return_metadata: If True, return additional metadata
            
        Returns:
            Dictionary with answer and optional metadata
        """
        print(f"\n🔍 Processing query: {chichewa_query}")
        
        # Step 1: Translate query to English
        print("   [1] Translating to English...")
        english_query = self.translator.translate_to_english(chichewa_query)
        print(f"   → English query: {english_query}")
        
        # Step 2: Classify query type
        print("   [2] Classifying query...")
        query_type = self.classify_query(english_query)
        print(f"   → Query type: {query_type}")
        
        # Step 3: Handle based on classification
        if query_type == "greeting":
            print("   [3] Handling as greeting")
            chichewa_answer = self.handle_greeting()
            
            return {
                "answer": chichewa_answer,
                "query_type": "greeting",
                "sources": [],
                "english_query": english_query
            }
        
        elif query_type == "out_of_scope":
            print("   [3] Handling as out-of-scope")
            chichewa_answer = self.handle_out_of_scope(chichewa_query)
            
            return {
                "answer": chichewa_answer,
                "query_type": "out_of_scope",
                "sources": [],
                "english_query": english_query
            }
        
        else:  # relevant query
            # Step 3: Retrieve relevant documents
            print("   [3] Retrieving relevant documents...")
            retrieved_docs = self.retrieve_documents(english_query)
            print(f"   → Retrieved {len(retrieved_docs)} documents")
            
            # Step 4: Generate answer in English
            print("   [4] Generating answer...")
            english_answer, sources = self.generate_answer(english_query, retrieved_docs)
            print(f"   → English answer: {english_answer[:100]}...")
            
            # Step 5: Translate answer to Chichewa
            print("   [5] Translating answer to Chichewa...")
            chichewa_answer = self.translator.translate_to_chichewa(english_answer)
            
            result = {
                "answer": chichewa_answer,
                "query_type": "relevant",
                "sources": sources,
                "english_query": english_query
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
    print("Testing Chichewa RAG Chatbot")
    print("=" * 70)
    
    # Initialize the RAG chain
    rag_chain = ChichewaRAGChain()
    
    # Test queries
    test_queries = [
        # Greeting
        "Moni, muli bwanji?",
        
        # Out of scope - weather
        "Kwacha bwanji lero?",
        
        # Out of scope - math
        "Kodi 2 + 2 ndi zingati?",
        
        # Relevant - news query
        "Kodi nkhani iyi ikukhudza chiyani?",
        
        # Relevant - specific query
        "Ndiuzeni za masewera"
    ]
    
    for query in test_queries:
        print("\n" + "=" * 70)
        result = rag_chain.answer_query(query, return_metadata=False)
        
        print(f"\n📥 Query (Chichewa):  {query}")
        print(f"🔍 Query Type:        {result['query_type']}")
        print(f"📤 Answer (Chichewa): {result['answer']}")
        
        if result['sources']:
            print(f"📚 Sources:           {', '.join(result['sources'])}")
    
    print("\n" + "=" * 70)
    print("Testing complete!")
    print("=" * 70)
