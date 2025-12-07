"""
Translator Module

This module handles translation between Chichewa and English using OpenAI GPT-4.
Uses zero-shot translation with clear system prompts.
"""

from typing import Optional
import re
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Banking product names that might appear in queries (case-insensitive)
PRODUCT_NAMES = [
    "amayi angathe", "mlimi", "fiestasave", "banknet", "mo626", "mo626ice",
    "fcda", "itf", "diaspora", "step up", "payday loan", "mortgage",
    "visa debit", "eft", "call account", "current account", "savings account",
    "fixed term deposit", "student serve", "special savers", "contactless card",
    "documentary", "standby letter", "custody services", "payment gateway",
    "consumer loan", "vehicle loan", "asset based", "employer guaranteed"
]


class Translator:
    """Handles Chichewa ↔ English translation using OpenAI GPT-4"""
    
    def __init__(
        self,
        model: str = "gpt-4",
        temperature: float = 0.3
    ):
        """
        Initialize the translator
        
        Args:
            model: OpenAI model to use (gpt-4 recommended for better Chichewa support)
            temperature: Lower for more consistent translations (0.0-1.0)
        """
        self.model = model
        self.temperature = temperature
        
        # Initialize the LLM
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=os.getenv("OPENAI_API_KEY")
        )
    
    def detect_language(self, text: str) -> str:
        """
        Detect the primary language of text (English or Chichewa)
        Handles mixed language queries and banking product names intelligently
        
        Args:
            text: Text to analyze
            
        Returns:
            Language code: "english" or "chichewa"
        """
        # Preprocess: Remove product names to avoid confusion
        cleaned_text = text.lower()
        for product in PRODUCT_NAMES:
            # Remove product names (case-insensitive)
            cleaned_text = re.sub(r'\b' + re.escape(product) + r'\b', '', cleaned_text, flags=re.IGNORECASE)
        
        # Remove extra whitespace
        cleaned_text = ' '.join(cleaned_text.split()).strip()
        
        # If very little text remains after removing product names, use original
        if len(cleaned_text) < 5:
            cleaned_text = text
        
        detection_prompt = """Determine the PRIMARY/PREDOMINANT language of the following text.

IMPORTANT:
- Ignore any banking product names (they may be in any language)
- Focus on the question words, verbs, and sentence structure
- Determine which language is PREDOMINANTLY used
- If mostly English words/structure → respond "english"
- If mostly Chichewa words/structure → respond "chichewa"  
- If unclear or mixed equally → respond "english" (default)

Text: {text}

Respond with ONLY ONE WORD: either "english" or "chichewa"."""
        
        messages = [
            HumanMessage(content=detection_prompt.format(text=cleaned_text))
        ]
        
        try:
            response = self.llm.invoke(messages)
            language = response.content.strip().lower()
            
            # Validate response
            if language not in ["english", "chichewa"]:
                # Default to English if unclear
                return "english"
            
            return language
        
        except Exception as e:
            print(f"Language detection error: {e}")
            return "english"  # Default to English on error (safer assumption)
    
    def translate_to_english(self, chichewa_text: str) -> str:
        """
        Translate Chichewa text to English
        
        Args:
            chichewa_text: Text in Chichewa language
            
        Returns:
            Translated text in English
        """
        system_prompt = (
            "You are a professional translator specializing in Chichewa and English. "
            "Translate the following text from Chichewa to English. "
            "Maintain the original meaning, tone, and context. "
            "Provide only the translation without any explanations or additional text."
        )
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=chichewa_text)
        ]
        
        try:
            response = self.llm.invoke(messages)
            translation = response.content.strip()
            return translation
        
        except Exception as e:
            print(f"Translation error (Chichewa→English): {e}")
            return f"[Translation failed: {chichewa_text}]"
    
    def translate_to_chichewa(self, english_text: str) -> str:
        """
        Translate English text to Chichewa with natural, conversational quality
        
        Args:
            english_text: Text in English language
            
        Returns:
            Translated text in natural, fluent Chichewa
        """
        system_prompt = """You are an expert Chichewa translator who speaks fluent, natural Chichewa.

Translate the following English text to Chichewa.

IMPORTANT GUIDELINES:
- Use NATURAL, EVERYDAY Chichewa that native speakers use in conversation
- Use proper Chichewa grammar and sentence structure
- Keep technical banking/financial terms in English where commonly used (e.g., "loan", "account", "MK", "ATM")
- Use conversational, friendly, and warm tone
- Ensure the translation sounds NATURAL and FLUENT, NOT literal/robotic/word-for-word
- Use simple present tense for direct statements (e.g., "Ndikufuna" not "Ndimafuna")

Examples of GOOD natural Chichewa:
- "I want" → "Ndikufuna" (NOT "Ndimafuna")
- "Hello" → Use context-appropriate greetings like "Zikuyenda bwanji" (informal), "Mwaswera bwanji" (afternoon), or just start without greeting
- "Thank you" → "Zikomo" or "Zikomo kwambiri"
- "Please note" → "Chonde dziwani" or "Onani kuti"
- "Available" → "alipo" or "zimapezeka"
- "I'm happy to help" → "Ndikondwera kukuthandizani"
- "We have different types" → "Tili ndi mitundu yosiyanasiyana" or "Kuli mitundu yosiyanasiyana"
- "You can" → "Mutha" or "Mungathe"
- "If you need" → "Ngati mukufuna" or "Ngati mufuna"

CRITICAL - Natural Conversation Starters (NEVER use "Moni"):
- Instead of "Hello," use: "Zikuyenda bwanji" (How's it going), "Mwaswera bwanji" (afternoon), "Wawa" (Hey - informal), or skip greeting and start directly with "Zikomo" or the main message
- For responses, often start with just "Zikomo kwambiri" or go straight to answering
- Keep it casual and conversational like native speakers

Translate to natural, conversational Chichewa (translation only, no explanations):"""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=english_text)
        ]
        
        try:
            response = self.llm.invoke(messages)
            translation = response.content.strip()
            
            # Post-process to make greetings more natural
            translation = self._naturalize_chichewa_greetings(translation)
            
            return translation
        
        except Exception as e:
            print(f"Translation error (English→Chichewa): {e}")
            return f"[Translation failed: {english_text}]"
    
    def _naturalize_chichewa_greetings(self, text: str) -> str:
        """
        Post-process Chichewa text to replace formal greetings with natural ones
        
        Args:
            text: Chichewa text that may contain formal greetings
            
        Returns:
            Text with more natural, conversational greetings
        """
        import random
        
        # Natural greeting alternatives for different contexts
        casual_greetings = [
            "Zikuyenda bwanji",  # How's it going
            "Zikomo kwambiri",   # Thank you very much (often used to start responses)
            "Wawa",              # Hey (very informal)
        ]
        
        # If text starts with "Moni" (too formal), replace with something more natural
        # Pattern: "Moni!" or "Moni," at the start
        if text.startswith("Moni!") or text.startswith("Moni,"):
            # For most banking responses, starting with "Zikomo kwambiri" or just removing "Moni" works best
            # We'll just remove "Moni," or "Moni!" and let the rest flow naturally
            if text.startswith("Moni!"):
                text = text.replace("Moni!", "", 1).strip()
            elif text.startswith("Moni,"):
                text = text.replace("Moni,", "", 1).strip()
        
        return text
    
    def translate_with_context(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        context: Optional[str] = None
    ) -> str:
        """
        Translate with additional context for better accuracy
        
        Args:
            text: Text to translate
            source_lang: Source language (e.g., "Chichewa" or "English")
            target_lang: Target language (e.g., "English" or "Chichewa")
            context: Optional context about the topic (e.g., "news article about sports")
            
        Returns:
            Translated text
        """
        context_info = f"\nContext: {context}" if context else ""
        
        system_prompt = (
            f"You are a professional translator specializing in {source_lang} and {target_lang}. "
            f"Translate the following text from {source_lang} to {target_lang}.{context_info} "
            "Maintain the original meaning, tone, and context. "
            "Provide only the translation without any explanations or additional text."
        )
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=text)
        ]
        
        try:
            response = self.llm.invoke(messages)
            translation = response.content.strip()
            return translation
        
        except Exception as e:
            print(f"Translation error ({source_lang}→{target_lang}): {e}")
            return f"[Translation failed: {text}]"


if __name__ == "__main__":
    # Test the translator
    print("=" * 60)
    print("Testing Chichewa ↔ English Translator")
    print("=" * 60)
    
    translator = Translator()
    
    # Test cases: Chichewa → English
    print("\n📝 Test 1: Chichewa → English")
    print("-" * 60)
    
    chichewa_phrases = [
        "Kodi nkhani iyi ikukhudza chiyani?",
        "Nanga zochitika zinali bwanji?",
        "Moni, muli bwanji?",
        "Ndikufuna kudziwa zambiri za nkhaniyi."
    ]
    
    for phrase in chichewa_phrases:
        print(f"\nChichewa: {phrase}")
        english = translator.translate_to_english(phrase)
        print(f"English:  {english}")
    
    # Test cases: English → Chichewa
    print("\n\n📝 Test 2: English → Chichewa")
    print("-" * 60)
    
    english_phrases = [
        "What is this article about?",
        "How many people were affected?",
        "Hello, how are you?",
        "I would like to know more about this news."
    ]
    
    for phrase in english_phrases:
        print(f"\nEnglish:  {phrase}")
        chichewa = translator.translate_to_chichewa(phrase)
        print(f"Chichewa: {chichewa}")
    
    # Test round-trip translation
    print("\n\n📝 Test 3: Round-trip Translation (Chichewa → English → Chichewa)")
    print("-" * 60)
    
    original = "Kodi anthu angati anakhudzidwa ndi chigamulochi?"
    print(f"\nOriginal (Chichewa):    {original}")
    
    english_version = translator.translate_to_english(original)
    print(f"Translated (English):   {english_version}")
    
    back_to_chichewa = translator.translate_to_chichewa(english_version)
    print(f"Back to Chichewa:       {back_to_chichewa}")
    
    # Test with context
    print("\n\n📝 Test 4: Translation with Context")
    print("-" * 60)
    
    query = "Kodi masewera anayenda bwanji?"
    context = "sports news article"
    
    print(f"\nChichewa: {query}")
    print(f"Context:  {context}")
    
    english_with_context = translator.translate_with_context(
        text=query,
        source_lang="Chichewa",
        target_lang="English",
        context=context
    )
    print(f"English:  {english_with_context}")
    
    print("\n" + "=" * 60)
    print("Translation tests complete!")
    print("=" * 60)
