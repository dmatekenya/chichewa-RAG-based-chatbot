# RAG Chatbot Improvement Plan

**Project**: Chichewa Banking Chatbot Quality Enhancement  
**Date**: December 7, 2025  
**Goal**: Achieve ChatGPT-level quality for Chichewa responses

---

## Executive Summary

This plan addresses the core quality issues in our Chichewa banking chatbot by improving both the RAG pipeline and Chichewa generation. Current issues include:

- **Incorrect Section Retrieval**: Queries about "Ubwino" (benefits) return requirements sections
- **Low Translation Quality**: Early attempts produced incomprehensible Chichewa
- **Poor Context Precision**: Retrieving wrong sections due to minimal metadata

**Completed Foundation Work**:
- ✅ Bilingual RAG (direct Chichewa generation, no back-translation)
- ✅ Product name preservation in translation
- ✅ Banking terminology handling (Ubwino=benefits, Phindu=interest)
- ✅ CSV phrase mappings (88 natural Chichewa phrases)

**Current Status**: Chichewa quality improved from incomprehensible → functional, but not ChatGPT-level yet.

---

## Problem Analysis

### Root Cause: Retrieval Precision
The chatbot retrieves wrong document sections because:
1. **Minimal Metadata**: Only stores `{source, file_path, file_type}`
2. **No Section Awareness**: Can't distinguish benefits vs requirements vs features
3. **Generic Retrieval**: No query intent detection to filter sections
4. **Suboptimal Chunking**: 1000-char chunks don't respect document structure

### Example Failure Case
```
Query: "Ubwino wa amayi angathe account" (Benefits of amayi angathe account)
Expected: Benefits section from amayi-angathe-account.pdf
Actual: Requirements section (wrong context)
Result: Answer lists requirements instead of benefits
```

---

## ChatGPT's Recommendations

### 1. Clean Knowledge Base
- **Section-Aware Chunking**: Parse PDFs by section headers (Benefits, Requirements, Features)
- **Optimal Chunk Size**: 250-400 tokens (currently 1000 chars)
- **Preserve Structure**: Keep section headers with chunks for context

### 2. Rich Metadata
Add to each chunk:
```python
metadata = {
    "source": "amayi-angathe-account.pdf",
    "product_name": "amayi angathe",
    "section_type": "benefits",  # or "requirements", "features", "general"
    "account_category": "savings",  # or "loan", "current"
    "chunk_number": 1
}
```

### 3. Better Retrieval
- **Upgrade Embeddings**: text-embedding-3-large (better semantic understanding)
- **Metadata Filtering**: Filter by section_type based on query intent
- **Reduce k**: From 5 → 3 for precision (with metadata filtering, less is more)
- **Optional Re-ranking**: Cohere or cross-encoder for relevance

### 4. Strong Prompts
- **Query Intent Detection**: Classify "Ubwino" → benefits, "Zofunikira" → requirements
- **Section-Specific Prompts**: Different templates for benefits vs features
- **Explicit Instructions**: "Only use information from benefits sections"

### 5. Two-Stage Generation
```
Stage 1 (Accuracy): Generate comprehensive answer in English from retrieved context
Stage 2 (Fluency): Translate to natural Chichewa using phrase mappings
```

---

## Implementation Options

### Option A: Quick Wins (1-2 hours)
**Minimal code changes for immediate improvement**

#### Session 1 Changes:
1. **Basic Metadata Enrichment**
   ```python
   # In document_processor.py
   product_name = extract_product_from_filename(file_path)
   metadata = {
       "source": file_path,
       "product_name": product_name,
       "file_type": "pdf"
   }
   ```

2. **Query Intent Detection**
   ```python
   # In rag_chain.py
   def detect_intent(query: str) -> str:
       if "ubwino" in query.lower():
           return "benefits"
       elif "zofunikira" in query.lower():
           return "requirements"
       return "general"
   ```

3. **Section-Aware Prompts**
   ```python
   if intent == "benefits":
       prompt += "\nFocus only on benefits and advantages."
   ```

**Impact**: 30-40% quality improvement with minimal risk

---

### Option B: Comprehensive Rebuild (2-3 weeks)
**Full implementation of all ChatGPT recommendations**

#### Phase 1: Knowledge Base (Week 1)
**Goal**: Section-aware document processing with rich metadata

**Tasks**:
1. **Section Detection in PDFs** (3-4 days)
   - Implement section header detection
   - Parse documents by structure
   - Create section-aware chunks

2. **Rich Metadata System** (2-3 days)
   - Add product_name, section_type, account_category
   - Update Document creation with full metadata
   - Rebuild vector store

3. **Chunk Optimization** (1 day)
   - Reduce to 250-400 tokens
   - Add section headers to chunks
   - Test chunk quality

#### Phase 2: Retrieval Enhancement (Week 2)
**Goal**: Precise, intent-aware retrieval

**Tasks**:
1. **Upgrade Embeddings** (1 day)
   - Switch to text-embedding-3-large
   - Rebuild embeddings
   - Compare retrieval quality

2. **Query Intent System** (2 days)
   - Implement intent classifier
   - Add metadata filters
   - Test intent detection accuracy

3. **Retrieval Optimization** (2 days)
   - Reduce k from 5 → 3
   - Add section prioritization
   - Optional: Implement re-ranking

#### Phase 3: Generation Enhancement (Week 3)
**Goal**: ChatGPT-level Chichewa fluency

**Tasks**:
1. **Two-Stage Generation** (2-3 days)
   - Stage 1: Accurate English answer
   - Stage 2: Natural Chichewa translation
   - Validate improvements

2. **Prompt Engineering** (2 days)
   - Section-specific templates
   - Enhanced phrase usage
   - Context-aware instructions

3. **Testing & Validation** (2-3 days)
   - Test suite for common queries
   - Compare with ChatGPT quality
   - User acceptance testing

**Total Effort**: 15-20 days of development

---

### Option C: Iterative Approach (Recommended)
**Balance quick wins with systematic improvement**

#### Sprint 1 (Week 1): Foundation
- Session 1: Quick wins from Option A (1-2 hours)
- Session 2: Basic section detection (2-3 days)
- Session 3: Rich metadata implementation (2 days)

**Deliverable**: 50-60% quality improvement, foundation for advanced features

#### Sprint 2 (Week 2): Retrieval
- Session 4: Upgrade embeddings (1 day)
- Session 5: Intent-based filtering (2-3 days)
- Session 6: Optimize k and test (1-2 days)

**Deliverable**: 70-80% quality improvement, precise retrieval

#### Sprint 3 (Week 3): Polish
- Session 7: Two-stage generation (2-3 days)
- Session 8: Prompt refinement (1-2 days)
- Session 9: Testing & iteration (2 days)

**Deliverable**: 90-95% of ChatGPT quality

---

## Why Option B Takes 2-3 Weeks

### PDF Section Detection Complexity

**It's not technically difficult, but requires careful engineering:**

#### 1. Document Structure Variety (2-3 days)
```
Challenge: Banking PDFs have inconsistent structures
- Some use "Benefits" vs "Product Benefits" vs "Advantages"
- Headers may be bold, larger font, or just capitalized
- Section boundaries aren't always clear
```

**Solution Approaches**:
- **Layout Analysis** (PyMuPDF, pdfplumber): Detect font size/weight changes
- **Pattern Matching**: Regex for common header patterns
- **ML-Based** (LayoutLM): Overkill for this project
- **Hybrid**: Combine layout + keywords

**Time Breakdown**:
- Day 1: Analyze current PDFs, identify patterns
- Day 2: Implement header detection
- Day 3: Test on all documents, handle edge cases

#### 2. Section Extraction Logic (1-2 days)
```python
# Not trivial because:
- Need to preserve context (header + content)
- Handle nested sections (benefits may have sub-bullets)
- Deal with tables, images spanning sections
- Ensure chunks don't break mid-sentence
```

**Challenges**:
- **Boundary Detection**: Where does "Benefits" end and "Requirements" start?
- **Context Preservation**: Include header in each chunk for clarity
- **Table Handling**: Benefits often in table format
- **Multi-column Layouts**: Some PDFs have 2-column layouts

**Time Breakdown**:
- Day 1: Implement section extraction
- Day 2: Handle edge cases (tables, multi-column)

#### 3. Metadata Mapping (1 day)
```python
# Product name extraction
"amayi-angathe-account.pdf" → "amayi angathe"
"mlimi-loan.pdf" → "mlimi"

# Section classification
"Benefits" → "benefits"
"Product Features" → "features"
"Eligibility" → "requirements"
```

**Challenges**:
- Filename inconsistencies (dashes vs spaces vs underscores)
- Section header variations (synonyms)
- Account category inference

#### 4. Testing & Validation (2-3 days)
**This is the real time sink:**
- Test on all 38 documents
- Verify sections detected correctly
- Check chunk quality (not too short/long)
- Validate metadata accuracy
- Handle documents that don't fit pattern
- Manual review of problematic cases

**Why It Takes Time**:
- 38 documents × 5 sections each = ~190 sections to verify
- Edge cases require manual inspection
- Iterate on detection logic based on failures
- Quality checks can't be fully automated

#### 5. Vector Store Rebuild (1 day)
- Delete old embeddings
- Reprocess all documents with new logic
- Generate new embeddings
- Verify retrieval works
- Compare before/after quality

### Total: 7-10 days for Section Detection Alone

**The PDF processing itself (2-3 hours) is easy.**  
**The engineering to handle all documents correctly (7-10 days) is what takes time.**

---

## Alternative: Faster Section Detection Approaches

### Approach 1: Keyword-Based (Faster - 2-3 days)
```python
def classify_section(text: str) -> str:
    text_lower = text.lower()
    
    # Benefits indicators
    if any(word in text_lower for word in ['benefit', 'advantage', 'ubwino']):
        return 'benefits'
    
    # Requirements indicators
    if any(word in text_lower for word in ['requirement', 'eligibility', 'zofunikira']):
        return 'requirements'
    
    # Features indicators
    if any(word in text_lower for word in ['feature', 'characteristic']):
        return 'features'
    
    return 'general'
```

**Pros**: Fast to implement, works for 80% of cases  
**Cons**: Less precise, may misclassify mixed sections

### Approach 2: LLM-Based Classification (Faster - 1-2 days)
```python
def classify_chunk_with_llm(chunk: str) -> dict:
    prompt = """
    Classify this banking document chunk:
    
    {chunk}
    
    Return JSON with:
    - section_type: benefits/requirements/features/general
    - confidence: 0-1
    """
    
    response = llm.invoke(prompt)
    return json.loads(response)
```

**Pros**: Very fast to implement, handles edge cases  
**Cons**: API costs, slower processing, less deterministic

### Approach 3: Hybrid (Recommended for Option C)
1. **Week 1**: Use keyword-based classification (2-3 days)
2. **Week 2**: Add layout analysis for headers (2 days)
3. **Week 3**: Refine based on user feedback (1-2 days)

**Total**: 5-7 days instead of 10 days

---

## Technical Implementation Details

### Current State
```python
# document_processor.py (CURRENT)
chunks = text_splitter.split_text(text)
for chunk in chunks:
    metadata = {
        "source": file_path,
        "file_path": file_path,
        "file_type": "pdf"
    }
    documents.append(Document(page_content=chunk, metadata=metadata))
```

### Target State (Option B - Full Implementation)
```python
# document_processor.py (TARGET)
sections = parse_pdf_by_sections(file_path)  # New function
for section in sections:
    chunks = section_aware_splitter.split(section.content)
    for i, chunk in enumerate(chunks):
        metadata = {
            "source": file_path,
            "product_name": extract_product_name(file_path),
            "section_type": section.type,  # benefits/requirements/features
            "section_header": section.header,  # "Product Benefits"
            "account_category": infer_category(file_path),  # savings/loan
            "chunk_number": i,
            "file_type": "pdf"
        }
        # Include section header in chunk for context
        content = f"{section.header}\n\n{chunk}"
        documents.append(Document(page_content=content, metadata=metadata))
```

### Retrieval Enhancement
```python
# rag_chain.py (TARGET)
def answer_query(query: str, language: str = "en") -> dict:
    # 1. Translate query to English
    english_query = translate_to_english(query)
    
    # 2. Detect intent
    intent = detect_query_intent(english_query)  # "benefits", "requirements", etc.
    
    # 3. Build metadata filter
    filter_dict = build_metadata_filter(english_query, intent)
    # Example: {"section_type": "benefits", "product_name": "amayi angathe"}
    
    # 4. Retrieve with filtering
    docs = vectorstore.similarity_search(
        english_query,
        k=3,  # Reduced from 5
        filter=filter_dict
    )
    
    # 5. Optional re-ranking
    if use_reranking:
        docs = rerank_documents(english_query, docs)
    
    # 6. Two-stage generation
    # Stage 1: Accurate English answer
    english_answer = generate_answer(english_query, docs, target_language="en")
    
    # Stage 2: Natural Chichewa translation
    if language == "ny":
        chichewa_answer = generate_answer(
            english_query, 
            docs, 
            target_language="ny",
            base_answer=english_answer  # For consistency
        )
        return chichewa_answer
    
    return english_answer
```

---

## Recommended Path Forward

### Start with Option C - Sprint 1, Session 1 (Today)

**Immediate Actions (1-2 hours)**:

1. **Add Basic Metadata** (30 min)
   ```python
   # Quick product extraction from filename
   def extract_product_from_filename(path: str) -> str:
       filename = os.path.basename(path)
       # "amayi-angathe-account.pdf" → "amayi angathe"
       return filename.replace('-', ' ').replace('.pdf', '').replace('account', '').strip()
   ```

2. **Implement Intent Detection** (30 min)
   ```python
   def detect_query_intent(query: str) -> str:
       query_lower = query.lower()
       if any(word in query_lower for word in ['ubwino', 'benefit', 'advantage']):
           return 'benefits'
       elif any(word in query_lower for word in ['zofunikira', 'requirement', 'eligibility']):
           return 'requirements'
       elif any(word in query_lower for word in ['mtengo', 'cost', 'fee', 'price']):
           return 'fees'
       return 'general'
   ```

3. **Add Intent to Prompts** (30 min)
   ```python
   if intent == "benefits":
       system_msg += "\nFocus ONLY on benefits and advantages. Ignore requirements."
   ```

**Expected Improvement**: 30-40% better answers immediately

### Next Week: Sprint 1, Sessions 2-3

**Session 2**: Implement keyword-based section classification (2-3 days)  
**Session 3**: Add rich metadata to vector store (2 days)

**Expected Improvement**: 50-60% of ChatGPT quality

---

## Success Metrics

### Before (Current State)
```
Query: "Ubwino wa amayi angathe account"
Response: Lists requirements instead of benefits
Quality: 40-50% of ChatGPT level
```

### After Sprint 1 (Week 1)
```
Query: "Ubwino wa amayi angathe account"
Response: Lists benefits with some requirements mixed in
Quality: 60-70% of ChatGPT level
```

### After Sprint 2 (Week 2)
```
Query: "Ubwino wa amayi angathe account"
Response: Lists only benefits, accurate content
Quality: 80-85% of ChatGPT level
```

### After Sprint 3 (Week 3)
```
Query: "Ubwino wa amayi angathe account"
Response: Natural Chichewa benefits list, well-structured
Quality: 90-95% of ChatGPT level
```

---

## Risk Assessment

### Option A (Quick Wins)
- **Risk**: Low - minimal changes
- **Impact**: Moderate (30-40% improvement)
- **Reversible**: Yes, easy to rollback

### Option B (Comprehensive)
- **Risk**: Medium - major refactoring
- **Impact**: High (90-95% improvement)
- **Reversible**: Difficult once vector store rebuilt

### Option C (Iterative) - RECOMMENDED
- **Risk**: Low-Medium - gradual changes
- **Impact**: High (cumulative to 90-95%)
- **Reversible**: Yes, can stop after any sprint

---

## Conclusion

**Recommended Approach**: Option C - Iterative Implementation

**Rationale**:
1. Quick wins in hours (Session 1)
2. Visible progress each week
3. Can stop at any sprint if quality is sufficient
4. Lower risk than full rebuild
5. Learn from each sprint to inform next steps

**PDF Section Detection Timeline**:
- Keyword-based: 2-3 days (good enough for most cases)
- Layout-based: +2-3 days (better precision)
- Full validation: +2-3 days (production ready)
- **Total**: 7-10 days for robust implementation

**Why It's Not Just "PDF Processing"**:
- Document structure variety requires custom handling
- Quality validation takes time (38 documents × multiple sections)
- Edge cases and iterative refinement
- Integration with existing pipeline
- Vector store rebuild and testing

**Next Step**: Implement Sprint 1, Session 1 quick wins today for immediate improvement.
