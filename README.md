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
- Created Python 3.13 virtual environment (`venv/`)
- Installed all dependencies (LangChain, OpenAI, ChromaDB, Streamlit, etc.)
- Set up project structure with `src/` and `data/` directories
- Created `.gitignore` for Python, vector store, and environment files

### Phase 2: Document Processing Pipeline ✓
- Created `src/document_processor.py` module
- Loaded 5 English newspaper articles from `data/docs/`:
  - sports-1.docx
  - Constitutions on paper.docx
  - 2 Shoprite shops-close.docx
  - Jane-Ansah.docx
  - celebrity-leaks.docx
- Split documents into 32 chunks (size: 1000 chars, overlap: 200)
- Created ChromaDB vector store with OpenAI embeddings
- Successfully tested document retrieval

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

## 🛠️ Technology Stack

- **Python**: 3.13
- **LLM**: OpenAI GPT-4 / GPT-3.5-turbo
- **Embeddings**: OpenAI text-embedding-3-small
- **Vector Store**: ChromaDB
- **Framework**: LangChain
- **UI**: Streamlit
- **Document Parsing**: python-docx

## 🚦 How to Resume Work

1. **Activate virtual environment**:
   ```bash
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
