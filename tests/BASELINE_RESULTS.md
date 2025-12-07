# Baseline Evaluation Results - BEFORE Session 1

**Date**: December 7, 2025
**Test**: Focused test on "Ubwino wa amayi angathe account"

## Query Details
- **Query (Chichewa)**: "Ubwino wa amayi angathe account"
- **Query (English)**: "Benefits of amayi angathe account"
- **Expected Intent**: benefits
- **Expected Behavior**: Should retrieve ONLY benefits section

## Results

### Detection & Classification
✅ **Language Detection**: chichewa (correct)
✅ **Translation**: "Benefits of amayi angathe account" (correct)
✅ **Intent Classification**: product_inquiry (correct - routes to RAG)

### Retrieved Documents
- Doc 1: Amayi Angathe Business Savings Account.pdf
- Doc 2: 233-amayi-angathe-factsheet.pdf
- Doc 3: 219-savings-account.pdf

**Total**: 5 documents retrieved (k=5)

### Generated Answer (Chichewa)

```
Amayi Angathe Business Savings Account imakhala ndi zofunika zambiri zomwe zingathandize maklienti. 
Zimene zi ndi zofunika zake:

1. Malonda aulere: Pali malonda aulere omwe mungapeze ngati mukulemba akaunti ya Amayi Angathe...

2. Kusamalira ndalama kochepa: Pali zinthu zina zomwe mungapange ndi akaunti ya Amayi Angathe...

3. Kusamalira ndalama zochepa: Pamene mukulemba akaunti ya Amayi Angathe, mungasamalire ndalama zochepa...

4. Malipiro aulere: Pali malipiro aulere omwe mungapanga ndi akaunti ya Amayi Angathe...
```

## Issues Identified

### ❌ Problem: Answer discusses "zofunika" (requirements) instead of "ubwino" (benefits)

The answer lists:
1. "zofunika" = requirements/needs (WRONG - should be benefits)
2. Focuses on minimum balance requirements
3. Discusses account opening requirements

**Root Cause**: Query asks for "ubwino" (benefits) but retrieved documents likely contain mixed sections. Without metadata filtering, the RAG system can't distinguish between:
- Benefits sections (ubwino, advantages, features)
- Requirements sections (zofunikira, eligibility)
- Fees sections (mtengo, charges)

### Expected vs Actual
- **Expected**: Benefits like free transactions, ATM card, interest rates, mobile banking access
- **Actual**: Requirements like minimum balance (MK3,000), monthly fees (MK200), EFT transaction procedures

## Session 1 Goals

Implement these changes to fix the issue:

1. **Query Intent Detection**: Detect that "ubwino" = benefits intent
2. **Metadata Enrichment**: Add product_name from filename  
3. **Intent-Aware Prompts**: Add instructions like "Focus ONLY on benefits, not requirements"

**Expected Improvement**: 30-40% better answers by reducing wrong-section retrieval

## Next Steps

1. Run full baseline evaluation on all 7 test queries
2. Implement Session 1 changes
3. Re-run evaluation and compare
4. Document improvement metrics
