"""
Chichewa Phrase Mappings

This module loads and provides natural Chichewa phrase mappings for the chatbot.
Used to guide LLM in generating natural, conversational Chichewa responses.
"""

import csv
import os
from typing import Dict, List, Optional


def load_phrase_mappings() -> Dict[str, Dict[str, str]]:
    """
    Load English-to-Chichewa phrase mappings from CSV
    
    Returns:
        Dictionary mapping English phrases to their Chichewa translations and context
    """
    phrases = {}
    csv_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data/translations/english_chichewa_phrases.csv"
    )
    
    try:
        with open(csv_path, 'r', encoding='utf-8-sig') as f:  # utf-8-sig removes BOM
            reader = csv.DictReader(f)
            for row in reader:
                phrases[row['english_phrase']] = {
                    'chichewa': row['chichewa_translation'],
                    'context': row.get('context_notes', ''),
                    'formality': row.get('formality_level', '')
                }
    except FileNotFoundError:
        print(f"Warning: Phrase mappings CSV not found at {csv_path}")
        return {}
    
    return phrases


def get_phrase_examples(category: str = 'all', limit: int = 10) -> List[str]:
    """
    Get example phrase translations for prompt engineering
    
    Args:
        category: Type of phrases to get (greetings, affirmations, etc.)
        limit: Maximum number of examples to return
        
    Returns:
        List of formatted example strings for prompts
    """
    phrases = load_phrase_mappings()
    examples = []
    
    # Common high-value examples for the prompt
    important_phrases = [
        'Sure', 'I understand', 'Thank you for asking', 'I can help with that',
        'Hello', 'Hi', 'We have', 'You can', 'For example',
        'Please note', 'If you have any questions', 'I hope this helps'
    ]
    
    for phrase in important_phrases:
        if phrase in phrases and phrases[phrase]['chichewa']:
            chichewa = phrases[phrase]['chichewa']
            # Skip SKIP and REPHRASE entries in examples
            if chichewa not in ['SKIP', 'REPHRASE']:
                # Format with alternatives if multiple options
                examples.append(f'"{phrase}" → "{chichewa}"')
                if len(examples) >= limit:
                    break
    
    return examples


def build_chichewa_generation_guidelines() -> str:
    """
    Build comprehensive guidelines for generating natural Chichewa responses
    
    Returns:
        Formatted string with translation guidelines and examples
    """
    examples = get_phrase_examples(limit=15)
    
    guidelines = """
CHICHEWA RESPONSE GUIDELINES:

1. NATURAL CONVERSATIONAL STYLE:
   - Use everyday Chichewa that native speakers use
   - Avoid word-for-word translations from English
   - Use natural sentence flow and structure
   - Be warm, friendly, and helpful

2. TECHNICAL TERMS:
   - Keep banking/financial terms in English (account, loan, ATM, MK, EFT, etc.)
   - Use Chichewa for explanations and connectors
   - Examples: "savings account", "mobile banking", "interest rate"

3. COMMON PHRASE TRANSLATIONS:
"""
    
    for example in examples:
        guidelines += f"   - {example}\n"
    
    guidelines += """
4. NATURAL CONNECTORS (use these liberally):
   - "komanso" (and also), "zomwe" (which), "moti" (so that)
   - "motsatira" (according to), "ndi uwu" (here they are)
   - "ndiye" (so/therefore), "kenako" (then/next)
   - "chifukwa" (because), "ngati" (if)

5. SKIP THESE (don't translate directly):
   - "Unfortunately" → just state the fact
   - "Actually" → restructure naturally
   - "Well" → skip or use "Ndiye"
   - Formal greetings → use casual ones or skip

6. OPENING RESPONSES:
   - Prefer starting directly with content
   - If greeting needed: "Zikomo" or context-specific greeting
   - NEVER use "Moni" (too formal/textbook)
   - Examples: "Zikuyenda bwanji", "Wawa", "Ndamva"

7. STRUCTURE:
   - Answer the question directly
   - Use bullet points for lists (with Chichewa explanations)
   - End helpfully (e.g., "Ngati muli ndi mafunso ena, mutha kufunsa")
"""
    
    return guidelines


if __name__ == "__main__":
    # Test the module
    print("Loading phrase mappings...")
    phrases = load_phrase_mappings()
    print(f"Loaded {len(phrases)} phrases\n")
    
    print("Sample mappings:")
    for phrase in ['Sure', 'I understand', 'Thank you for asking', 'Hello']:
        if phrase in phrases:
            print(f"{phrase}: {phrases[phrase]['chichewa']}")
    
    print("\n" + "="*70)
    print(build_chichewa_generation_guidelines())
