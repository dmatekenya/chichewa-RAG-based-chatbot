"""
Streamlit App for Chichewa RAG Chatbot

A chat interface for asking questions in Chichewa about English news articles.
Includes rate limiting to prevent API abuse.
"""

import streamlit as st
from datetime import datetime, timedelta
from collections import defaultdict
import sys
from pathlib import Path
import json
import hashlib

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.rag_chain import ChichewaRAGChain


# Configuration
MAX_QUERIES_PER_SESSION = 20  # Maximum queries per session
MAX_QUERIES_PER_HOUR = 10     # Maximum queries per hour per user
RATE_LIMIT_WINDOW = 3600      # 1 hour in seconds


class RateLimiter:
    """Simple rate limiter to track query usage"""
    
    def __init__(self):
        if 'rate_limiter_data' not in st.session_state:
            st.session_state.rate_limiter_data = {
                'session_count': 0,
                'hourly_queries': [],
                'session_start': datetime.now()
            }
    
    def can_make_query(self) -> tuple[bool, str]:
        """
        Check if user can make another query
        
        Returns:
            Tuple of (can_query: bool, message: str)
        """
        data = st.session_state.rate_limiter_data
        now = datetime.now()
        
        # Check session limit
        if data['session_count'] >= MAX_QUERIES_PER_SESSION:
            return False, f"Mwaposa muyeso wa mafunso mu session iyi ({MAX_QUERIES_PER_SESSION} mafunso). Chonde yambitsaninso tsamba."
        
        # Clean old queries (older than 1 hour)
        cutoff_time = now - timedelta(seconds=RATE_LIMIT_WINDOW)
        data['hourly_queries'] = [
            q for q in data['hourly_queries'] 
            if q > cutoff_time
        ]
        
        # Check hourly limit
        if len(data['hourly_queries']) >= MAX_QUERIES_PER_HOUR:
            return False, f"Mwaposa muyeso wa mafunso pa ola ({MAX_QUERIES_PER_HOUR} mafunso pa ola). Chonde yesani mu ola limene likubweralo."
        
        return True, ""
    
    def record_query(self):
        """Record a new query"""
        data = st.session_state.rate_limiter_data
        data['session_count'] += 1
        data['hourly_queries'].append(datetime.now())
        st.session_state.rate_limiter_data = data
    
    def get_usage_stats(self) -> dict:
        """Get current usage statistics"""
        data = st.session_state.rate_limiter_data
        return {
            'session_queries': data['session_count'],
            'session_limit': MAX_QUERIES_PER_SESSION,
            'hourly_queries': len(data['hourly_queries']),
            'hourly_limit': MAX_QUERIES_PER_HOUR,
            'session_duration': (datetime.now() - data['session_start']).seconds // 60
        }


def initialize_session_state():
    """Initialize Streamlit session state"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'rag_chain' not in st.session_state:
        with st.spinner('Kukhazikitsa chatbot... (Initializing chatbot...)'):
            try:
                st.session_state.rag_chain = ChichewaRAGChain()
            except FileNotFoundError:
                # Vector store doesn't exist - create it on first run
                st.info("🔄 Kukonza mauthenga kwa nthawi yoyamba... (Processing documents for first time...)")
                from src.document_processor import DocumentProcessor
                processor = DocumentProcessor()
                processor.process_documents(force_recreate=True)
                st.session_state.rag_chain = ChichewaRAGChain()
                st.success("✅ Chatbot wokonzeka! (Chatbot ready!)")
    
    if 'rate_limiter' not in st.session_state:
        st.session_state.rate_limiter = RateLimiter()


def display_chat_message(role: str, content: str, metadata: dict = None):
    """Display a chat message with optional metadata"""
    with st.chat_message(role):
        st.markdown(content)
        
        if metadata and metadata.get('sources'):
            with st.expander("📚 Magwero (Sources)"):
                for source in metadata['sources']:
                    st.caption(f"• {source}")


def clear_chat_history():
    """Clear chat history"""
    st.session_state.messages = []
    st.session_state.rate_limiter_data = {
        'session_count': 0,
        'hourly_queries': [],
        'session_start': datetime.now()
    }


def main():
    """Main Streamlit app"""
    
    # Page configuration
    st.set_page_config(
        page_title="Chichewa News Chatbot",
        page_icon="💬",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        st.title("ℹ️ Zambiri (About)")
        
        st.markdown("""
        ### Chichewa News Chatbot
        
        Muli bwanji! Ndine chatbot yemwe amathandiza kuyankha mafunso pa nkhani za mauthenga mu Chichewa.
        
        **Mukhoza kundifunsa:**
        - Za zochitika mu nkhani
        - Za anthu mu mauthenga
        - Za masewera
        - Za ndale
        - Nkhani zina zonse
        
        ---
        
        Hello! I'm a chatbot that helps answer questions about news articles in Chichewa.
        
        **You can ask me about:**
        - Events in the news
        - People in the articles
        - Sports
        - Politics
        - Other news topics
        """)
        
        # Usage statistics
        st.markdown("---")
        st.markdown("### 📊 Kagwiritsidwe (Usage)")
        
        stats = st.session_state.rate_limiter.get_usage_stats()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Mafunso (Queries)",
                f"{stats['session_queries']}/{stats['session_limit']}"
            )
        with col2:
            st.metric(
                "Pa Ola (Per Hour)",
                f"{stats['hourly_queries']}/{stats['hourly_limit']}"
            )
        
        st.caption(f"⏱️ Session: {stats['session_duration']} min")
        
        # Clear chat button
        st.markdown("---")
        if st.button("🗑️ Chotsani Mauthenga (Clear Chat)", use_container_width=True):
            clear_chat_history()
            st.rerun()
        
        # Footer
        st.markdown("---")
        st.caption("Built with LangChain + OpenAI + Streamlit")
    
    # Main chat interface
    st.title("💬 Chichewa News Chatbot")
    st.caption("Funsani mafunso mu Chichewa pa nkhani za mauthenga (Ask questions in Chichewa about news articles)")
    
    # Display chat history
    for message in st.session_state.messages:
        display_chat_message(
            message['role'],
            message['content'],
            message.get('metadata')
        )
    
    # Chat input
    if prompt := st.chat_input("Lembani funso lanu mu Chichewa... (Type your question in Chichewa...)"):
        
        # Check rate limit
        can_query, limit_message = st.session_state.rate_limiter.can_make_query()
        
        if not can_query:
            # Display rate limit message
            st.error(limit_message)
            st.stop()
        
        # Add user message to chat
        st.session_state.messages.append({
            'role': 'user',
            'content': prompt
        })
        display_chat_message('user', prompt)
        
        # Get response from RAG chain
        with st.chat_message('assistant'):
            with st.spinner('Ndikuganiza... (Thinking...)'):
                try:
                    result = st.session_state.rag_chain.answer_query(
                        prompt,
                        return_metadata=False
                    )
                    
                    answer = result['answer']
                    
                    # Display answer
                    st.markdown(answer)
                    
                    # Display sources if available
                    if result.get('sources'):
                        with st.expander("📚 Magwero (Sources)"):
                            for source in result['sources']:
                                st.caption(f"• {source}")
                    
                    # Record the query
                    st.session_state.rate_limiter.record_query()
                    
                    # Add assistant message to chat
                    st.session_state.messages.append({
                        'role': 'assistant',
                        'content': answer,
                        'metadata': {
                            'sources': result.get('sources', []),
                            'query_type': result.get('query_type', 'unknown')
                        }
                    })
                
                except Exception as e:
                    error_message = "Pepani, panali vuto. Chonde yesani kwa nthawi. (Sorry, there was an error. Please try again.)"
                    st.error(error_message)
                    st.error(f"Technical details: {str(e)}")
                    
                    # Add error message to chat
                    st.session_state.messages.append({
                        'role': 'assistant',
                        'content': error_message
                    })
    
    # Welcome message for new users
    if len(st.session_state.messages) == 0:
        with st.chat_message('assistant'):
            st.markdown("""
            👋 **Moni! Muli bwanji?**
            
            Ndine chatbot yemwe amathandiza pa nkhani za mauthenga. Funsani mafunso mu Chichewa!
            
            **Zitsanzo za mafunso:**
            - "Kodi nkhani iyi ikukhudza chiyani?"
            - "Ndiuzeni za masewera"
            - "Anthu angati anakhudzidwa?"
            
            ---
            
            👋 **Hello! How are you?**
            
            I'm a chatbot that helps with news articles. Ask questions in Chichewa!
            
            **Example questions:**
            - "What is this story about?"
            - "Tell me about sports"
            - "How many people were affected?"
            """)


if __name__ == "__main__":
    main()
