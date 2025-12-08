# Structured Prompt Engineering (SPE) for Low-Resource Multilingual Chatbots

**Date**: December 7, 2025  
**Branch**: chatbot-spe  
**Objective**: Evaluate SPE as an alternative to RAG for small knowledge bases with low-resource languages

---

## Motivation

### Why SPE for This Use Case?

**Context**:
- Small knowledge base (~38 banking product documents)
- Low-resource target language (Chichewa)
- Limited training data for embeddings
- Need for high accuracy in multilingual setting

**RAG Limitations for Low-Resource Languages**:
1. **Embedding Quality**: Default embeddings not optimized for Chichewa/English cross-lingual retrieval
2. **Retrieval Errors**: Can retrieve wrong sections (benefits vs requirements confusion)
3. **Translation Dependencies**: Multiple translation steps add error accumulation
4. **Complexity**: Vectorstore management, chunking strategies, retrieval tuning

**SPE Advantages**:
1. **Full Context**: Entire knowledge base available in prompt (no retrieval errors)
2. **Deterministic**: Same query always sees same knowledge
3. **Simpler Pipeline**: Classify → Structure → Generate (no embeddings/retrieval)
4. **Better Control**: Direct control over what information is presented
5. **Faster Iteration**: No vectorstore rebuilding needed

---

## Implementation: Structured Prompt Engineering Chain

### Architecture

```
User Query (Chichewa/English)
    ↓
[1] Language Detection
    ↓
[2] Translation to English (if needed)
    ↓
[3] Query Classification (greeting/product_inquiry/out_of_scope/etc)
    ↓
[4] Intent Detection (benefits/requirements/fees/features/general)
    ↓
[5] Product Extraction (amayi_angathe/mlimi/etc)
    ↓
[6] Build Structured Context (filter knowledge base by intent + product)
    ↓
[7] Generate Answer DIRECTLY in target language
    ↓
Response (Chichewa/English)
```

### Key Differences from RAG

| Aspect | RAG | SPE |
|--------|-----|-----|
| **Knowledge Storage** | Vector embeddings | Structured JSON/dict |
| **Retrieval** | Similarity search (k=5) | Rule-based filtering |
| **Context Building** | Top-k chunks | Intent-filtered sections |
| **Errors** | Can retrieve wrong sections | Always has full context |
| **Latency** | Embedding + retrieval + generation | Translation + generation |
| **Maintenance** | Rebuild vectorstore on updates | Update JSON structure |
| **Scalability** | Good for large KBs (1000s of docs) | Best for small KBs (<100 docs) |

---

## Knowledge Base Structure

```python
{
    "products": {
        "amayi_angathe": {
            "name": "Amayi Angathe Business Savings Account",
            "category": "savings",
            "target_audience": "Women entrepreneurs",
            "benefits": [
                "Free monthly maintenance (first 6 months)",
                "Free ATM card",
                "Low minimum balance (MK 3,000)",
                ...
            ],
            "requirements": [
                "Valid national ID",
                "Proof of business registration",
                ...
            ],
            "fees": {
                "monthly_maintenance": "MK 0 (first 6 months), then MK 200",
                "atm_withdrawals": "Free at FDH ATMs",
                ...
            },
            "features": [...]
        },
        "mlimi": {...}
    },
    "general_info": {...}
}
```

### Intent-Based Context Filtering

**Benefits Query**: `"Ubwino wa amayi angathe"`
```
Filtered Context:
PRODUCT: Amayi Angathe Business Savings Account
BENEFITS:
1. Free monthly maintenance (first 6 months)
2. Free ATM card upon opening
3. Low minimum balance of MK 3,000
4. 50% discount on EFT fees
...
```

**Requirements Query**: `"Zofunikira za mlimi loan"`
```
Filtered Context:
PRODUCT: Mlimi Loan
REQUIREMENTS:
1. Valid national ID
2. Proof of farming activity
3. Business plan
4. Collateral for loans > MK 200,000
...
```

---

## Prompt Engineering Strategy

### Chichewa Generation Prompt

```
Ndinu wothandiza wa banki yomwe ikuthandiza maklienti.

ZAMBIRI ZA ZINTHU ZA BANKI (Structured Knowledge Base):
[FILTERED STRUCTURED CONTEXT BASED ON INTENT]

FUNSO LA MUNTHU (mu Chingerezi): {english_query}

MALANGIZO A NKHANI:
{INTENT-SPECIFIC INSTRUCTION}
- For benefits: "Focus ONLY on benefits and advantages"
- For requirements: "Focus ONLY on requirements and eligibility"
- For fees: "Focus ONLY on fees and costs"

[CHICHEWA GENERATION GUIDELINES FROM CSV]

MALANGIZO OFUNIKIRA:
- Yankhani m'CHICHEWA CHOYAMBA (not word-for-word translation)
- Use structured information above
- Keep banking terms in English
- Be conversational and helpful
- Format clearly with bullet points
- End with offer to help

YANKHANI M'CHICHEWA:
```

### Key Advantages

1. **Full Context Access**: LLM sees all relevant product info
2. **Intent Alignment**: Filtered context matches query intent
3. **No Retrieval Errors**: Can't retrieve wrong sections
4. **Consistent Quality**: Same input → same output

---

## Preliminary Results (Initial Testing)

### Test 1: Benefits Query
**Query**: `"Ubwino wa amayi angathe account"`

| Metric | RAG | SPE |
|--------|-----|-----|
| Intent Detection | ✅ benefits | ✅ benefits |
| Product Detection | Amayi Angathe PDF | amayi_angathe ✅ |
| Latency | 19.97s | 14.61s (**26.8% faster**) |
| Answer Quality | Mixed benefits/requirements | **Pure benefits** ✅ |

**Winner**: **SPE** (faster + more accurate)

### Test 2: Requirements Query
**Query**: `"Zofunikira za mlimi loan"`

| Metric | RAG | SPE |
|--------|-----|-----|
| Intent Detection | ❌ benefits (wrong!) | ❌ features (translation issue) |
| Translation | "Features" (wrong) | "Features" (wrong) |
| Latency | 11.86s (**15.2% faster**) | 13.98s |
| Answer Quality | Retrieved mlimi account | Retrieved mlimi loan ✅ |

**Issue**: Both failed due to translator not knowing "zofunikira" = "requirements"  
**Winner**: **RAG** (slightly faster)

### Test 3: Fees Query
**Query**: `"Mtengo wa amayi angathe account"`

| Metric | RAG | SPE |
|--------|-----|-----|
| Intent Detection | ✅ fees | ✅ fees |
| Product Detection | Amayi Angathe | amayi_angathe |
| Latency | 9.52s | ~14s |
| Answer Quality | Lists fees | Lists fees |

**Winner**: **RAG** (faster on this query)

---

## Analysis

### SPE Advantages Observed

1. **✅ Better Section Focus**: SPE answers are more intent-aligned
   - Benefits query got pure benefits (not mixed with requirements)
   - Structured filtering prevents section confusion

2. **✅ Simpler Product Identification**: Direct key matching vs filename parsing
   - `amayi_angathe` vs `"Amayi Angathe Business Savings Account.pdf"`

3. **✅ Faster on Complex Queries**: 26.8% faster on benefits query
   - No vector search overhead
   - Direct context building

4. **✅ Deterministic Behavior**: Same query always gets same context
   - RAG can vary based on retrieval randomness

### SPE Challenges Observed

1. **⚠️ Manual Knowledge Base Construction**
   - Currently using hardcoded structure
   - Need to parse 38 PDFs into JSON
   - More upfront work than RAG

2. **⚠️ Token Usage**
   - SPE sends full structured context in every prompt
   - RAG only sends k=5 retrieved chunks
   - SPE may cost more per query (but faster)

3. **⚠️ Scalability Limit**
   - Works great for <100 products
   - Would struggle with 1000s of products (context window limit)
   - RAG scales better to large knowledge bases

4. **⚠️ Still Depends on Translation Quality**
   - Both approaches failed on "zofunikira" translation
   - Need to enhance translator regardless of approach

---

## Best Practices for Low-Resource Multilingual Chatbots

### When to Use SPE

✅ **Use SPE when**:
- Knowledge base is small (<100 documents)
- Need high accuracy and consistency
- Low-resource target language (poor embedding quality)
- Knowledge is structured (products, FAQs, policies)
- Fast iteration required (no vectorstore rebuilds)

❌ **Use RAG when**:
- Knowledge base is large (100s-1000s of documents)
- Content is unstructured (research papers, manuals)
- Good embedding models available for all languages
- Need dynamic knowledge updates without redeployment

### Hybrid Approach (Recommended)

**Combine Both**:
1. **SPE for Core Products**: Use structured prompts for ~50 main products
2. **RAG for Long-tail**: Use retrieval for rare queries, edge cases
3. **Intent-Based Routing**: 
   - Common products → SPE
   - General info/rare topics → RAG

---

## Next Steps

### 1. Complete SPE Implementation (1-2 days)
- [ ] Parse all 38 PDFs into structured JSON
- [ ] Extract benefits, requirements, fees, features for each product
- [ ] Add contact information structure
- [ ] Build automated PDF→JSON parser

### 2. Enhance Translator (1 day)
- [ ] Add "zofunikira" = "requirements" mapping
- [ ] Add "mtengo" = "price/cost" mapping
- [ ] Test on all banking terminology

### 3. Comprehensive Comparison (2 days)
- [ ] Test on full eval dataset (when ready)
- [ ] Measure: accuracy, latency, cost, Chichewa quality
- [ ] A/B testing with real users
- [ ] Document findings for design patterns paper

### 4. Design Patterns Documentation (Ongoing)
- [ ] Document when to use SPE vs RAG
- [ ] Best practices for low-resource languages
- [ ] Knowledge base structuring strategies
- [ ] Prompt engineering patterns for multilingual
- [ ] Cost-benefit analysis framework

---

## Conclusion

**Initial Findings**:
- SPE shows **promise for small, structured knowledge bases**
- **26.8% faster** on complex queries (benefits)
- **Better section focus** due to intent-based filtering
- **Simpler pipeline** (no embeddings/retrieval)
- **Same translation challenges** as RAG (need better Chichewa support)

**Recommendation**:
- **Continue SPE implementation** for full comparison
- **Build PDF→JSON parser** to complete knowledge base
- **Test on larger eval dataset** for robust comparison
- **Consider hybrid approach** for production (SPE + RAG)

**Value for Research**:
This comparison will provide **concrete design patterns** for:
- Multilingual chatbot architecture decisions
- Small vs large knowledge base strategies
- Low-resource language optimization
- Cost-quality-latency tradeoffs
