# Chichewa-English RAG Chatbot

A RAG-based chatbot that reads English documents but interacts with users in Chichewa language.

## 🎯 Project Goal

Build a chatbot where:
- **Documents**: English newspaper articles
- **User Interaction**: Questions and answers in Chichewa
- **Technology**: OpenAI models + LangChain + ChromaDB

## 📋 Architecture

```
User Query (Chichewa) 
    ↓
[1] Translate to English
    ↓
[2] Retrieve relevant chunks from English docs (RAG)
    ↓
[3] Generate answer in English using context
    ↓
[4] Translate answer back to Chichewa
    ↓
Response (Chichewa)
```

## ✅ Completed Phases

### Phase 1: Environment Setup ✓
**Status:** Complete  
**Files Created:**
- `requirements.txt` - Python dependencies
- `.gitignore` - Excludes venv, secrets, vector store
- Virtual environment with Python 3.13

**What it does:**
- Sets up isolated Python environment
- Installs LangChain, OpenAI, ChromaDB, Streamlit, python-docx
- Configures project structure

### Phase 2: Document Processing Pipeline ✓
**Status:** Complete  
**Files Created:**
- `src/document_processor.py` - Document loading and vector store creation

**What it does:**
## 🎉 Project Complete!

All phases have been successfully completed and the chatbot is deployed!

### Optional Future Enhancements

These features could be added in the future:

1. **Conversation Memory**
   - Multi-turn conversation tracking
   - Context awareness across questions
   - User session history

2. **Enhanced Translation**
   - Domain-specific glossary for news terms
   - Few-shot examples for better quality
   - Translation caching to reduce API costs

3. **Advanced Features**
   - Language auto-detection (Chichewa vs English)
   - Support for mixed-language queries
   - Voice input/output in Chichewa

4. **Performance Optimization**
   - Query result caching
   - Faster model options (GPT-3.5-turbo)
   - Batch processing for efficiency

5. **Analytics**
   - Usage analytics dashboard
   - Popular query tracking
   - Translation quality feedback

6. **Content Management**
   - Admin interface to add/remove documents
   - Automatic document updates
   - Multi-language document support chiyani?" → "What is this story about?"
- ✅ "How many people were affected?" → "Anthu angati anakhudzidwa?"
- ✅ Round-trip translation maintains meaning

### Phase 4: RAG Chain Implementation ✓
**Status:** Complete  
**Files Created:**
- `src/rag_chain.py` - Complete RAG pipeline with smart query handling

**What it does:**
1. **Query Classification** - Categorizes queries into:
   - Greetings ("Moni, muli bwanji?") → Friendly welcome
   - Out-of-scope ("Kwacha bwanji lero?") → Polite redirect
   - Relevant ("Ndiuzeni za masewera") → Full RAG pipeline

2. **Complete Flow for Relevant Queries:**
   - Translate Chichewa query → English
   - Retrieve top 3 relevant document chunks
   - Generate answer using GPT-4 with context
   - Translate answer back to Chichewa
   - Return with source attribution

3. **Graceful Error Handling:**
   - Doesn't crash on out-of-scope questions
   - Provides helpful responses in Chichewa
   - Guides users to ask relevant questions

**Test results:**
- ✅ Greetings handled with prompts about available topics
- ✅ Weather/math questions politely declined with redirect
- ✅ News queries answered accurately with sources
- ✅ All responses in natural Chichewa

### Phase 5: User Interface (Streamlit App) ✓
**Status:** Complete  
**Files Created:**
- `app.py` - Main Streamlit application
## 📊 Project Status

- ✅ Phase 1: Environment Setup
- ✅ Phase 2: Document Processing Pipeline
- ✅ Phase 3: Translation Layer (Chichewa ↔ English)
- ✅ Phase 4: RAG Chain Implementation
- ✅ Phase 5: Streamlit User Interface
- ✅ Phase 6: Deployment to Streamlit Cloud

**🎉 Project Status: COMPLETE & DEPLOYED**
  - 10 queries per hour per user
  - User-friendly messages in Chichewa when limits reached
- **Usage Dashboard:** Real-time stats in sidebar
  - Session query count
  - Hourly usage
  - Session duration
- **Source Attribution:** Shows which documents were used
- **Clear Chat:** Reset conversation history
- **Error Handling:** Graceful error messages in Chichewa
- **Bilingual UI:** Labels in both Chichewa and English

**Security features:**
- API keys stored as secrets (not in code)
- `.streamlit/secrets.toml` in `.gitignore`
- Ready for Streamlit Cloud deployment

### Phase 6: Deployment ✓
**Status:** Complete (Deployed to Streamlit Community Cloud)  
**Files Updated:**
- `app.py` - Auto-creates vector store if missing
- `src/rag_chain.py` - Handles missing vector store gracefully
- `DEPLOYMENT.md` - Step-by-step deployment instructions

**What it does:**
- **Auto-deployment:** Streamlit Cloud watches GitHub repo
- **Automatic Setup:** Creates vector store on first run
- **Persistent Storage:** Vector store saved between restarts
- **Zero-config:** No manual setup needed after secrets configured

**Deployment fixes:**
- Vector store auto-created from documents on first deployment
- Documents included in GitHub repo
- Secrets configured in Streamlit Cloud dashboard

**Live App:**
- Hosted on Streamlit Community Cloud
- Public URL accessible to anyone
- No API keys required from users
- Rate limiting protects against abuse

## 🚀 Next Steps

### Phase 3: Translation Layer (NEXT)
- Create `src/translator.py` module
- Implement Chichewa ↔ English translation using OpenAI GPT-4
- Use zero-shot translation with clear system prompts
- Test translation quality with sample phrases

### Phase 4: RAG Chain Implementation
- Create `src/rag_chain.py` module
- Build complete query flow:
  1. Translate Chichewa query to English
  2. Retrieve relevant document chunks
  3. Generate English answer with context
  4. Translate answer back to Chichewa
- Add conversation memory for multi-turn chats

### Phase 5: User Interface
- Create `app.py` with Streamlit UI
- Chat interface in Chichewa
- Display source citations
- Show conversation history

### Phase 6: Quality Enhancements
- Add LangSmith monitoring (already configured in `.env`)
- Implement language detection
- Fine-tune prompts for better translation
- Add caching for translations

## 📁 Project Structure

```
rag-demo-chichewa/
├── .env                        # API keys (OpenAI, LangSmith)
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── PROGRESS.md                 # Detailed progress tracking
├── venv/                       # Python 3.13 virtual environment
├── data/
│   ├── docs/                   # English source documents (5 .docx files)
│   └── vectorstore/            # ChromaDB vector store (32 chunks)
├── src/
│   └── document_processor.py   # Document loading & vector store
└── app.py                      # (To be created) Streamlit UI
```
## 🚀 How to Use

### Run Locally

1. **Activate virtual environment**:
   ```bash
   cd /Users/dmatekenya/git-repos/rag-demo-chichewa
   source venv/bin/activate
   ```

2. **Run Streamlit app**:
   ```bash
   streamlit run app.py
   # Or use the helper script:
   ./run_app.sh
   ```

3. **Access the app**:
   - Open browser to `http://localhost:8501`
   - Start chatting in Chichewa!

### Test Individual Components

```bash
# Test document processing
## 📝 Important Notes

### Local Development
- Vector store created automatically on first run
- Documents in `data/docs/` are processed into embeddings
- All API keys stored in `.env` and `.streamlit/secrets.toml` (not in git)
- LangSmith tracing enabled for debugging

### Deployment
- Vector store auto-created on Streamlit Cloud first run
- Takes ~30-60 seconds on first deployment to process documents
- Subsequent restarts are fast (vector store persists)
- Auto-redeploys when you push to GitHub

### Rate Limiting
- **Session limit:** 20 queries maximum
- **Hourly limit:** 10 queries per hour per user
- Protects against excessive API costs
- User-friendly messages in Chichewa when limits reached

### Cost Monitoring
- Monitor usage at: https://platform.openai.com/usage
- Estimated cost: ~$0.012 per query
- Set spending limits in OpenAI dashboard
- Consider stricter rate limits if costs are high

### Security
- ✅ API keys never exposed to users
- ✅ Secrets in `.gitignore`
- ✅ Environment variables used for all sensitive data
- ✅ Rate limiting prevents abuse
python src/rag_chain.py
```

### Deploy to Streamlit Cloud

See detailed instructions in `DEPLOYMENT.md`

Quick steps:
1. Push code to GitHub ✅ (already done)
2. Go to https://share.streamlit.io
3. Connect your repo
4. Add API keys in secrets
5. Deploy!
   cd /Users/dmatekenya/git-repos/rag-demo-chichewa
   source venv/bin/activate
   ```

2. **Test existing setup**:
   ```bash
   python src/document_processor.py
   ```

3. **Start Phase 3** (Translation Layer):
   - See `PROGRESS.md` for detailed next steps

## 📊 Current Status

- ✅ Phase 1: Environment Setup (Complete)
- ✅ Phase 2: Document Processing (Complete)
- 🔄 Phase 3: Translation Layer (Next)
- ⏳ Phase 4: RAG Chain (Pending)
- ⏳ Phase 5: User Interface (Pending)
- ⏳ Phase 6: Enhancements (Pending)

## 📝 Notes

- Vector store is persistent - documents only need to be processed once
- To recreate vector store: Use `force_recreate=True` in `document_processor.py`
- All API keys are stored in `.env` file (not committed to git)
- LangSmith tracing is enabled for debugging
