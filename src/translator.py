"""
Translator Module

This module handles translation between Chichewa and English using OpenAI GPT-4.
Uses zero-shot translation with clear system prompts.
"""

from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


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
        Translate English text to Chichewa
        
        Args:
            english_text: Text in English language
            
        Returns:
            Translated text in Chichewa
        """
        system_prompt = (
            "You are a professional translator specializing in Chichewa and English. "
            "Translate the following text from English to Chichewa. "
            "Maintain the original meaning, tone, and context. "
            "Use natural, conversational Chichewa that native speakers would understand. "
            "Provide only the translation without any explanations or additional text."
        )
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=english_text)
        ]
        
        try:
            response = self.llm.invoke(messages)
            translation = response.content.strip()
            return translation
        
        except Exception as e:
            print(f"Translation error (English→Chichewa): {e}")
            return f"[Translation failed: {english_text}]"
    
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
