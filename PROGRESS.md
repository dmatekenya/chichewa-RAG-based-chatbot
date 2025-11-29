# Project Progress Tracker

Last Updated: November 29, 2025

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
- Persistent vector store (no need to recreate)
- Option to force recreation if needed
- Error handling for missing files

---

## Phase 3: Translation Layer 🔄 NEXT PHASE

### Objective:
Create a translation module to handle Chichewa ↔ English translation using OpenAI GPT-4.

### Tasks To Do:

1. ⏳ Create `src/translator.py` module with:
   - `Translator` class
   - Method: `translate_to_english(chichewa_text: str) -> str`
   - Method: `translate_to_chichewa(english_text: str) -> str`
   - Use GPT-4 with zero-shot prompts
   - Clear system prompts for translation

2. ⏳ Implement translation prompts:
   ```python
   # Chichewa → English
   system_prompt = "You are a translator. Translate the following text from Chichewa to English. Maintain the original meaning and tone."
   
   # English → Chichewa
   system_prompt = "You are a translator. Translate the following text from English to Chichewa. Maintain the original meaning and tone."
   ```

3. ⏳ Test translation with sample phrases:
   - "Kodi nkhani iyi ikukhudza chiyani?" → "What is this article about?"
   - "Nanga zochitika zinali bwanji?" → "What happened?"
   - Test reverse translation quality

4. ⏳ Add error handling:
   - Handle API errors
   - Fallback for failed translations
   - Logging for debugging

### Files to Create:
- `src/translator.py`
- Test script or add tests to module

### Implementation Notes:
- Start with GPT-4 for best quality
- Use zero-shot (no examples needed initially)
- If quality insufficient, add few-shot examples or glossary
- Keep translation prompts simple and clear

---

## Phase 4: RAG Chain Implementation ⏳ PENDING

### Objective:
Build the complete RAG pipeline with translation integration.

### Tasks To Do:

1. ⏳ Create `src/rag_chain.py` module with:
   - `ChichewaRAGChain` class
   - Integration of translator + document retriever + LLM

2. ⏳ Implement query flow:
   ```python
   def answer_query(chichewa_query: str) -> str:
       # 1. Translate query to English
       english_query = translator.translate_to_english(chichewa_query)
       
       # 2. Retrieve relevant chunks
       docs = vectorstore.similarity_search(english_query, k=3)
       
       # 3. Generate answer in English
       english_answer = llm.generate(context=docs, query=english_query)
       
       # 4. Translate answer to Chichewa
       chichewa_answer = translator.translate_to_chichewa(english_answer)
       
       return chichewa_answer
   ```

3. ⏳ Add conversation memory:
   - Store chat history
   - Maintain context across turns
   - Use `ConversationBufferMemory` or similar

4. ⏳ Add source citation:
   - Track which documents were used
   - Include metadata in response

5. ⏳ Test end-to-end flow:
   - Sample Chichewa questions
   - Verify answer quality
   - Check source attribution

### Files to Create:
- `src/rag_chain.py`

---

## Phase 5: User Interface ⏳ PENDING

### Objective:
Create a Streamlit web app for chat interface.

### Tasks To Do:

1. ⏳ Create `app.py` with Streamlit:
   - Chat interface
   - Message history display
   - Input box for Chichewa queries

2. ⏳ Features to implement:
   - Display conversation history
   - Show source documents used
   - Clear chat button
   - Session state management

3. ⏳ UI elements:
   - Title: "Chichewa News Chatbot"
   - Sidebar: Settings, about info
   - Main area: Chat messages
   - Input: Text box + send button

4. ⏳ Run and test:
   ```bash
   streamlit run app.py
   ```

### Files to Create:
- `app.py`

---

## Phase 6: Quality Enhancements ⏳ PENDING

### Optional Improvements:

1. ⏳ Add language detection:
   - Auto-detect if user inputs English vs Chichewa
   - Handle mixed-language inputs

2. ⏳ Improve translation:
   - Add domain-specific glossary
   - Few-shot examples for better quality
   - Cache translations to reduce API calls

3. ⏳ LangSmith integration:
   - Already configured in `.env`
   - Add trace logging
   - Monitor translation quality

4. ⏳ Performance optimization:
   - Cache frequent queries
   - Batch translations if possible
   - Reduce API costs

5. ⏳ Better error handling:
   - Graceful degradation
   - User-friendly error messages in Chichewa

---

## How to Resume Development

### Quick Start:
```bash
cd /Users/dmatekenya/git-repos/rag-demo-chichewa
source venv/bin/activate
```

### Verify Setup:
```bash
# Test document processor
python src/document_processor.py

# Should show: Vector store loaded, retrieval working
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
