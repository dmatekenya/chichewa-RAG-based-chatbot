# Project Progress Tracker

**Project Status:** ✅ **COMPLETE & DEPLOYED**  
Last Updated: November 30, 2025

**Live App:** Deployed on Streamlit Community Cloud  
**Repository:** https://github.com/dmatekenya/chichewa-RAG-based-chatbot

---

## Phase 1: Environment Setup ✅ COMPLETE

### Tasks Completed:
1. ✅ Created project directory structure
   - `src/` for source code modules
   - `data/vectorstore/` for vector embeddings
   
2. ✅ Created `requirements.txt` with dependencies:
   ```
   langchain==0.3.7
   langchain-openai==0.2.8
   langchain-community==0.3.7
   chromadb==0.5.20
   python-docx==1.1.2
   streamlit==1.40.1
   python-dotenv==1.0.1
   ```

3. ✅ Created Python 3.13 virtual environment
   ```bash
   python3.13 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. ✅ Created `.gitignore`
   - Excludes: venv/, data/vectorstore/, .env, __pycache__, etc.

### Files Created:
- `requirements.txt`
- `.gitignore`

---

## Phase 2: Document Processing Pipeline ✅ COMPLETE

### Tasks Completed:
1. ✅ Created `src/document_processor.py` module with:
   - `DocumentProcessor` class
   - `.docx` file loader using `python-docx`
   - Text splitting with `RecursiveCharacterTextSplitter`
   - Vector store creation with ChromaDB + OpenAI embeddings
   - Persistent storage in `data/vectorstore/`

2. ✅ Processed 5 English newspaper articles:
   - sports-1.docx
   - Constitutions on paper.docx
   - 2 Shoprite shops-close.docx
   - Jane-Ansah.docx
   - celebrity-leaks.docx

3. ✅ Created vector store:
   - 32 text chunks (1000 chars each, 200 overlap)
   - OpenAI embeddings: `text-embedding-3-small`
   - Saved to: `data/vectorstore/`

4. ✅ Tested retrieval:
   ```
   Query: "What happened in the news?"
   Result: Successfully retrieved relevant chunks from documents
   ```

### Files Created:
- `src/document_processor.py`
- `data/vectorstore/` (ChromaDB database)

### Key Features Implemented:
- Automatic loading of all .docx files from directory
- Metadata tracking (source filename)
---

## Phase 3: Translation Layer ✅ COMPLETE

### Objective:
Create a translation module to handle Chichewa ↔ English translation using OpenAI GPT-4.

### Tasks Completed:

1. ✅ Created `src/translator.py` module with:
   - `Translator` class using GPT-4
   - Method: `translate_to_english(chichewa_text: str) -> str`
   - Method: `translate_to_chichewa(english_text: str) -> str`
   - Method: `translate_with_context()` for domain-specific translation
   - Zero-shot translation with clear system prompts
   - Temperature = 0.3 for consistent results

2. ✅ Implemented translation prompts:
   - Chichewa → English: "You are a professional translator..."
   - English → Chichewa: "...Use natural, conversational Chichewa..."
   - Clear instructions to maintain meaning and tone

3. ✅ Tested translation with sample phrases:
   - "Kodi nkhani iyi ikukhudza chiyani?" → "What is this story about?" ✓
   - "Moni, muli bwanji?" → "Hello, how are you?" ✓
   - "How many people were affected?" → "Anthu angati anakhudzidwa?" ✓
   - Round-trip translation maintains meaning ✓

4. ✅ Added error handling:
   - API error catching
   - Fallback messages for failed translations
   - Graceful degradation

### Files Created:
- `src/translator.py` (complete with tests)

### Test Results:
All translation tests passed successfully. GPT-4 provides high-quality Chichewa translations without requiring few-shot examples or glossaries.

---

## Phase 4: RAG Chain Implementation ✅ COMPLETE

### Objective:
Build the complete RAG pipeline with translation integration and smart query handling.

### Tasks Completed:

1. ✅ Created `src/rag_chain.py` module with:
   - `ChichewaRAGChain` class
   - Integration of translator + document retriever + LLM
   - Smart query classification system

2. ✅ Implemented complete query flow:
   ```python
   def answer_query(chichewa_query: str) -> dict:
       # 1. Translate query to English
       english_query = translator.translate_to_english(chichewa_query)
       
       # 2. Classify query type (greeting/out-of-scope/relevant)
       query_type = classify_query(english_query)
       
       # 3a. Handle greetings
       if greeting: return friendly_welcome_in_chichewa()
       
       # 3b. Handle out-of-scope queries
       if out_of_scope: return polite_redirect_in_chichewa()
       
       # 3c. Handle relevant queries (full RAG)
       if relevant:
           # Retrieve relevant chunks
           docs = vectorstore.similarity_search(english_query, k=3)
           
           # Generate answer in English with context
           english_answer = llm.generate(context=docs, query=english_query)
           
           # Translate answer to Chichewa
           chichewa_answer = translator.translate_to_chichewa(english_answer)
           
           return {answer, sources, metadata}
   ```

3. ✅ Added query classification:
   - GPT-4 classifier with temperature=0.0
   - Categories: "greeting", "out_of_scope", "relevant"
   - Consistent classification across queries

4. ✅ Implemented graceful handling:
   - Greetings: Warm welcome + prompt about topics
   - Out-of-scope (weather, math, etc.): Polite decline + redirect
   - Relevant: Full RAG pipeline with sources

5. ✅ Added source citation:
   - Tracks which documents were used
   - Returns source filenames
   - Metadata available for UI display

6. ✅ Tested end-to-end flow:
   - "Moni, muli bwanji?" → Greeting handled ✓
   - "Kwacha bwanji lero?" → Out-of-scope handled ✓
   - "Kodi 2 + 2 ndi zingati?" → Out-of-scope handled ✓
   - "Kodi nkhani iyi ikukhudza chiyani?" → RAG pipeline works ✓
   - "Ndiuzeni za masewera" → Returns sports info with sources ✓

### Files Created:
- `src/rag_chain.py` (complete with query classification)

### Key Achievement:
The chatbot gracefully handles ALL query types without crashing, providing helpful responses in Chichewa for every scenario.

---

## Phase 5: User Interface ✅ COMPLETE

### Objective:
Create a Streamlit web app with chat interface and rate limiting.

### Tasks Completed:

1. ✅ Created `app.py` with Streamlit:
   - Full chat interface
   - Message history display
   - Input box for Chichewa queries
   - Session state management

2. ✅ Implemented rate limiting:
   - `RateLimiter` class
   - Session limit: 20 queries maximum
   - Hourly limit: 10 queries per hour per user
   - User-friendly error messages in Chichewa
   - Real-time tracking of usage

3. ✅ Built UI features:
   - **Title:** "Chichewa News Chatbot"
   - **Sidebar:** 
     - About section (bilingual)
     - Usage statistics dashboard
     - Clear chat button
     - Built with info
   - **Main area:** 
     - Chat message history
     - Loading spinners with Chichewa text
     - Source attribution in expandable sections
   - **Input:** Text box with Chichewa placeholder

4. ✅ Added error handling:
   - Graceful API error messages
   - User-friendly error text in Chichewa
   - Technical details for debugging

5. ✅ Created deployment files:
   - `.streamlit/secrets.toml.example` - Template for API keys
   - `run_app.sh` - Helper script for local testing
   - Updated `.gitignore` to exclude secrets

6. ✅ Tested locally:
   - App runs at `http://localhost:8501`
   - All features working
   - Rate limiting functional
   - Chichewa interactions smooth

### Files Created:
- `app.py` - Main Streamlit application
- `run_app.sh` - Local testing helper
- `.streamlit/secrets.toml.example` - Secrets template
- Updated `.gitignore`

### User Experience:
- Clean, bilingual interface
- Real-time usage tracking
- Smooth chat experience
- Protected against abuse with rate limiting

---

## Phase 6: Deployment ✅ COMPLETE

### Objective:
Deploy to Streamlit Community Cloud and ensure automatic setup.

### Tasks Completed:

1. ✅ Created comprehensive deployment documentation:
   - `DEPLOYMENT.md` with step-by-step instructions
   - Streamlit Cloud setup guide
   - Local testing procedures
   - Security best practices
   - Cost monitoring guidance
   - Troubleshooting section

2. ✅ Fixed deployment issues:
   - Vector store auto-creation on first run
   - Updated `app.py` to handle missing vector store
   - Updated `src/rag_chain.py` to create vectorstore if needed
   - Documents included in GitHub repo

3. ✅ Configured auto-deployment:
   - GitHub repository connected to Streamlit Cloud
   - Auto-redeploy on push to main branch
   - Secrets configured in Streamlit Cloud dashboard
   - Vector store persists between restarts

4. ✅ Security implementation:
   - API keys stored as Streamlit secrets
   - `.streamlit/secrets.toml` in `.gitignore`
   - No sensitive data in GitHub repo
   - Rate limiting protects against abuse

5. ✅ Successfully deployed:
   - App live on Streamlit Community Cloud
   - Public URL accessible
   - No API keys required from users
   - First-run document processing working
   - Subsequent loads fast

### Files Created/Updated:
- `DEPLOYMENT.md` - Complete deployment guide
- `app.py` - Auto-creates vector store if missing
- `src/rag_chain.py` - Graceful vector store handling
- `.gitignore` - Excludes secrets

### Deployment Features:
- **Zero-config:** Auto-setup on first deployment
- **Auto-deploy:** Updates when GitHub changes
- **Persistent:** Vector store saved between restarts
- **Secure:** API keys protected
- **Cost-protected:** Rate limiting prevents abuse

### Cost Estimates:
- ~$0.012 per query
- With 10 queries/hour/user limit
- Manageable costs with built-in protection

---

## Summary: All Phases Complete! 🎉

### What We Built:

**A fully functional Chichewa-English RAG chatbot that:**
- ✅ Reads English newspaper articles
- ✅ Answers questions in Chichewa
- ✅ Handles greetings and out-of-scope queries gracefully
- ✅ Provides source attribution
- ✅ Has rate limiting for cost protection
- ✅ Is deployed and publicly accessible
- ✅ Auto-updates from GitHub

### Technology Stack:
- **Backend:** Python 3.13, LangChain, OpenAI GPT-4
- **Vector Store:** ChromaDB with OpenAI embeddings
- **Frontend:** Streamlit
- **Hosting:** Streamlit Community Cloud
- **Documents:** 5 English newspaper articles (.docx)

### Key Innovations:
1. **Smart Query Classification** - Handles any type of query
2. **Zero-shot Translation** - No training data required
3. **Auto-deployment** - Creates vector store on first run
4. **Rate Limiting** - Protects against API cost overruns
5. **Bilingual UX** - Chichewa & English throughout

### Files Structure:
```
rag-demo-chichewa/
├── app.py                      # Streamlit UI (main app)
├── run_app.sh                  # Local testing script
├── requirements.txt            # Python dependencies
├── README.md                   # Project overview (updated)
├── PROGRESS.md                 # This file
├── DEPLOYMENT.md               # Deployment guide
├── .env                        # Local environment variables
├── .gitignore                  # Git exclusions
├── data/
│   ├── docs/                   # 5 English .docx files
│   └── vectorstore/            # ChromaDB (auto-created)
├── src/
│   ├── document_processor.py   # Document loading & embeddings
│   ├── translator.py           # Chichewa ↔ English translation
│   └── rag_chain.py            # Complete RAG pipeline
└── .streamlit/
    ├── secrets.toml            # API keys (local, not in git)
    └── secrets.toml.example    # Template for secrets
```

---

## Future Enhancement Ideas

While the project is complete, these optional features could be added:

### Phase 7 (Optional): Advanced Features
```

### Start Phase 3:
Create `src/translator.py` with the translation logic.

---

## Resources & References

### API Keys (in `.env`):
- `OPENAI_API_KEY`: For GPT-4 and embeddings
- `LANGSMITH_API_KEY`: For tracing/monitoring
- `LANGSMITH_TRACING`: Set to `true`

### Documentation:
- LangChain: https://python.langchain.com/
- OpenAI API: https://platform.openai.com/docs
- ChromaDB: https://docs.trychroma.com/
- Streamlit: https://docs.streamlit.io/

### Key Design Decisions:
1. **Translation Strategy**: Zero-shot with GPT-4 (simple, no training data needed)
2. **Vector Store**: ChromaDB (lightweight, persistent, local)
3. **Embeddings**: OpenAI text-embedding-3-small (good quality, cost-effective)
4. **Chunk Size**: 1000 characters with 200 overlap (balanced for context)
5. **UI Framework**: Streamlit (quick to build, interactive)

---

## Notes & Reminders

- Vector store is already created and persistent - no need to reprocess documents unless adding new ones
- To add new documents: Place in `data/docs/` and run with `force_recreate=True`
- All environment variables are in `.env` (not tracked in git)
- Python 3.13 is required - virtual environment already set up
- Translation quality can be improved later if needed with few-shot examples
