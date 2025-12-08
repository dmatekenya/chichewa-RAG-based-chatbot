"""
Comparison Test: RAG vs Structured Prompt Engineering (SPE)

Evaluates both approaches on the same queries to compare:
- Answer quality
- Accuracy
- Latency
- Cost (token usage)
- Chichewa fluency
"""

import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag_chain import ChichewaRAGChain
from src.spe_chain import StructuredPromptChain

# Test queries covering different intents
TEST_QUERIES = [
    {
        "query_ny": "Ubwino wa amayi angathe account",
        "query_en": "Benefits of amayi angathe account",
        "expected_intent": "benefits",
        "expected_product": "amayi angathe"
    },
    {
        "query_ny": "Zofunikira za mlimi loan",
        "query_en": "Requirements for mlimi loan",
        "expected_intent": "requirements",
        "expected_product": "mlimi"
    },
    {
        "query_ny": "Mtengo wa amayi angathe account",
        "query_en": "Cost of amayi angathe account",
        "expected_intent": "fees",
        "expected_product": "amayi angathe"
    }
]


def run_comparison():
    """Run side-by-side comparison of RAG vs SPE."""
    
    print("\n" + "=" * 80)
    print("  RAG vs STRUCTURED PROMPT ENGINEERING (SPE) - Comparison")
    print("=" * 80)
    
    # Initialize both chains
    print("\n📦 Initializing chains...")
    rag_chain = ChichewaRAGChain()
    spe_chain = StructuredPromptChain()
    print("✅ Both chains initialized\n")
    
    results = []
    
    for i, test in enumerate(TEST_QUERIES, 1):
        print("\n" + "=" * 80)
        print(f"TEST {i}/{len(TEST_QUERIES)}")
        print("=" * 80)
        print(f"Query (Chichewa): {test['query_ny']}")
        print(f"Query (English):  {test['query_en']}")
        print(f"Expected Intent:  {test['expected_intent']}")
        print(f"Expected Product: {test['expected_product']}")
        
        # Test RAG approach
        print("\n" + "-" * 80)
        print("🔍 RAG APPROACH")
        print("-" * 80)
        
        start_time = time.time()
        rag_result = rag_chain.answer_query(test['query_ny'])
        rag_latency = time.time() - start_time
        
        print(f"\n📊 RAG Results:")
        print(f"   Intent:   {rag_result.get('query_intent', 'N/A')}")
        print(f"   Product:  {rag_result.get('sources', ['N/A'])[0] if rag_result.get('sources') else 'N/A'}")
        print(f"   Latency:  {rag_latency:.2f}s")
        print(f"\n   Answer:\n   {rag_result['answer'][:300]}...\n")
        
        # Test SPE approach
        print("-" * 80)
        print("📝 STRUCTURED PROMPT ENGINEERING (SPE) APPROACH")
        print("-" * 80)
        
        start_time = time.time()
        spe_result = spe_chain.answer_query(test['query_ny'])
        spe_latency = time.time() - start_time
        
        print(f"\n📊 SPE Results:")
        print(f"   Intent:   {spe_result.get('query_intent', 'N/A')}")
        print(f"   Product:  {spe_result.get('product', 'N/A')}")
        print(f"   Latency:  {spe_latency:.2f}s")
        print(f"\n   Answer:\n   {spe_result['answer'][:300]}...\n")
        
        # Comparison
        print("-" * 80)
        print("📈 COMPARISON")
        print("-" * 80)
        print(f"Intent Match RAG: {'✅' if rag_result.get('query_intent') == test['expected_intent'] else '❌'}")
        print(f"Intent Match SPE: {'✅' if spe_result.get('query_intent') == test['expected_intent'] else '❌'}")
        print(f"Latency: RAG={rag_latency:.2f}s vs SPE={spe_latency:.2f}s")
        print(f"Winner (Speed): {'RAG' if rag_latency < spe_latency else 'SPE'} ({'%.1f%%' % (abs(rag_latency - spe_latency) / max(rag_latency, spe_latency) * 100)} faster)")
        
        results.append({
            "query": test['query_ny'],
            "expected_intent": test['expected_intent'],
            "rag": {
                "intent": rag_result.get('query_intent'),
                "answer": rag_result['answer'],
                "latency": rag_latency
            },
            "spe": {
                "intent": spe_result.get('query_intent'),
                "answer": spe_result['answer'],
                "latency": spe_latency
            }
        })
    
    # Summary
    print("\n\n" + "=" * 80)
    print("  SUMMARY")
    print("=" * 80)
    
    rag_avg_latency = sum(r['rag']['latency'] for r in results) / len(results)
    spe_avg_latency = sum(r['spe']['latency'] for r in results) / len(results)
    
    rag_intent_accuracy = sum(1 for r in results if r['rag']['intent'] == r['expected_intent']) / len(results) * 100
    spe_intent_accuracy = sum(1 for r in results if r['spe']['intent'] == r['expected_intent']) / len(results) * 100
    
    print(f"\n📊 Intent Detection Accuracy:")
    print(f"   RAG: {rag_intent_accuracy:.0f}%")
    print(f"   SPE: {spe_intent_accuracy:.0f}%")
    
    print(f"\n⚡ Average Latency:")
    print(f"   RAG: {rag_avg_latency:.2f}s")
    print(f"   SPE: {spe_avg_latency:.2f}s")
    
    print(f"\n🏆 Winner:")
    if rag_intent_accuracy > spe_intent_accuracy:
        print(f"   Intent Accuracy: RAG (+{rag_intent_accuracy - spe_intent_accuracy:.0f}%)")
    elif spe_intent_accuracy > rag_intent_accuracy:
        print(f"   Intent Accuracy: SPE (+{spe_intent_accuracy - rag_intent_accuracy:.0f}%)")
    else:
        print(f"   Intent Accuracy: TIE")
    
    if rag_avg_latency < spe_avg_latency:
        print(f"   Speed: RAG ({(spe_avg_latency - rag_avg_latency) / spe_avg_latency * 100:.1f}% faster)")
    else:
        print(f"   Speed: SPE ({(rag_avg_latency - spe_avg_latency) / rag_avg_latency * 100:.1f}% faster)")
    
    print("\n" + "=" * 80)
    print("\n💡 Manual Quality Assessment Required:")
    print("   - Chichewa fluency")
    print("   - Answer completeness")
    print("   - Factual accuracy")
    print("   - User satisfaction")
    print("\n" + "=" * 80)
    
    return results


if __name__ == "__main__":
    run_comparison()
