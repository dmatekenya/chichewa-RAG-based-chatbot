"""
Simple evaluation script for Session 1 improvements.

Tests query intent detection and section retrieval accuracy.
Run BEFORE and AFTER Session 1 to measure improvement.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rag_chain import ChichewaRAGChain

# Initialize RAG chain
rag_chain = ChichewaRAGChain()

# Core test cases covering different intents
TEST_QUERIES = [
    {
        "id": 1,
        "query_ny": "Ubwino wa amayi angathe account",
        "query_en": "Benefits of amayi angathe account",
        "expected_intent": "benefits",
        "product": "amayi angathe",
        "description": "Should retrieve ONLY benefits section, not requirements"
    },
    {
        "id": 2,
        "query_ny": "Ndiuzeni za ubwino wa mlimi loan",
        "query_en": "Tell me about benefits of mlimi loan",
        "expected_intent": "benefits",
        "product": "mlimi",
        "description": "Should focus on advantages/benefits"
    },
    {
        "id": 3,
        "query_ny": "Zofunikira za amayi angathe account",
        "query_en": "Requirements for amayi angathe account",
        "expected_intent": "requirements",
        "product": "amayi angathe",
        "description": "Should retrieve ONLY requirements/eligibility, not benefits"
    },
    {
        "id": 4,
        "query_ny": "Zofunikira za mlimi loan ndi chani?",
        "query_en": "What are the requirements for mlimi loan?",
        "expected_intent": "requirements",
        "product": "mlimi",
        "description": "Should focus on eligibility criteria"
    },
    {
        "id": 5,
        "query_ny": "Mtengo wa savings account",
        "query_en": "Cost of savings account",
        "expected_intent": "fees",
        "product": "savings",
        "description": "Should retrieve fees/charges section"
    },
    {
        "id": 6,
        "query_ny": "Kodi amayi angathe account ndi chani?",
        "query_en": "What is amayi angathe account?",
        "expected_intent": "general",
        "product": "amayi angathe",
        "description": "General question - can retrieve mixed sections"
    },
    {
        "id": 7,
        "query_ny": "Phindu pa mlimi loan",
        "query_en": "Interest on mlimi loan",
        "expected_intent": "fees",
        "product": "mlimi",
        "description": "Should retrieve interest rate/fees information"
    },
]


def run_evaluation(phase="BASELINE"):
    """Run evaluation and display results."""
    
    print(f"\n{'=' * 80}")
    print(f"  {phase} EVALUATION - Session 1")
    print(f"{'=' * 80}\n")
    
    results = []
    
    for i, test in enumerate(TEST_QUERIES, 1):
        print(f"\n[Test {test['id']}/{len(TEST_QUERIES)}]")
        print(f"Query (Chichewa): {test['query_ny']}")
        print(f"Query (English):  {test['query_en']}")
        print(f"Expected Intent:  {test['expected_intent']}")
        print(f"Product:          {test['product']}")
        print(f"Description:      {test['description']}")
        print("-" * 80)
        
        try:
            # Run query (language is auto-detected)
            result = rag_chain.answer_query(test['query_ny'])
            
            # Display answer
            answer = result.get('answer', 'No answer generated')
            print(f"\nAnswer (Chichewa):")
            print(f"{answer[:300]}...")
            print()
            
            # Display retrieved context (first doc only for brevity)
            if 'source_documents' in result and result['source_documents']:
                print(f"Retrieved Context (first chunk):")
                first_doc = result['source_documents'][0].page_content
                print(f"{first_doc[:200]}...")
                print()
            
            # Manual assessment prompt
            print("ASSESSMENT:")
            print(f"1. Does the answer focus on {test['expected_intent']}? (benefits/requirements/fees/general)")
            print(f"2. Is the Chichewa natural and fluent?")
            print(f"3. Does it correctly address the question?")
            print()
            
            results.append({
                "test_id": test['id'],
                "query": test['query_ny'],
                "intent": test['expected_intent'],
                "answer": answer,
                "success": None  # Manual assessment
            })
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            results.append({
                "test_id": test['id'],
                "query": test['query_ny'],
                "intent": test['expected_intent'],
                "error": str(e),
                "success": False
            })
        
        print("=" * 80)
    
    # Summary
    print(f"\n{'=' * 80}")
    print(f"  EVALUATION COMPLETE - {phase}")
    print(f"{'=' * 80}")
    print(f"\nTotal tests run: {len(TEST_QUERIES)}")
    print(f"\nPlease manually assess each answer and record:")
    print(f"  - Intent accuracy (benefits/requirements/fees matched?)")
    print(f"  - Section precision (no mixing of benefits with requirements?)")
    print(f"  - Chichewa quality (natural and fluent?)")
    print()
    
    return results


def run_focused_test(query_ny: str, expected_intent: str):
    """Run a single focused test for quick iteration."""
    
    rag_chain = ChichewaRAGChain()
    
    print(f"\n{'=' * 60}")
    print(f"  FOCUSED TEST")
    print(f"{'=' * 60}")
    print(f"Query:           {query_ny}")
    print(f"Expected Intent: {expected_intent}")
    print("-" * 60)
    
    result = rag_chain.answer_query(query_ny)
    
    print(f"\nAnswer:")
    print(result.get('answer', 'No answer'))
    print()
    
    if 'source_documents' in result and result['source_documents']:
        print(f"\nRetrieved Documents ({len(result['source_documents'])}):")
        for i, doc in enumerate(result['source_documents'], 1):
            print(f"\n[Doc {i}] Source: {doc.metadata.get('source', 'unknown')}")
            print(f"Content: {doc.page_content[:200]}...")
    elif 'sources' in result and result['sources']:
        print(f"\nRetrieved Documents ({len(result['sources'])}):")
        for i, source in enumerate(result['sources'], 1):
            print(f"\n[Doc {i}]")
            print(f"Content: {source[:200]}...")
            
    print()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run evaluation tests")
    parser.add_argument(
        "--phase",
        default="BASELINE",
        help="Evaluation phase: BASELINE or AFTER_SESSION_1"
    )
    parser.add_argument(
        "--focused",
        action="store_true",
        help="Run focused test on 'Ubwino wa amayi angathe account'"
    )
    
    args = parser.parse_args()
    
    if args.focused:
        run_focused_test(
            "Ubwino wa amayi angathe account",
            "benefits"
        )
    else:
        run_evaluation(phase=args.phase)
