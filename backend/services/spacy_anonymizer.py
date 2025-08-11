import re
import hashlib
import logging
from typing import Dict, Tuple, List
import spacy

logger = logging.getLogger(__name__)

class SpacyAnonymizer:
    """
    Advanced anonymizer using spaCy's Named Entity Recognition (NER)
    for more accurate detection of sensitive data
    """
    
    def __init__(self):
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
            print("✅ spaCy model loaded successfully")
        except OSError:
            print("❌ spaCy model not found. Please run: python -m spacy download en_core_web_sm")
            raise
        
        # Patterns for additional sensitive data types
        self.patterns = {
            'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'PHONE': r'\b(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b',
            'SSN': r'\b\d{3}-\d{2}-\d{4}\b',
            'CREDIT_CARD': r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
            'IP_ADDRESS': r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',
            'DATE': r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{4}-\d{2}-\d{2}\b',
        }
        
        # spaCy entity types to anonymize
        self.entity_types = {
            'PERSON': 'NAME',
            'ORG': 'ORGANIZATION', 
            'GPE': 'LOCATION',  # Countries, cities, states
            'LOC': 'LOCATION',  # Non-GPE locations
            'FAC': 'FACILITY',  # Buildings, airports, highways
            'PRODUCT': 'PRODUCT',
            'EVENT': 'EVENT',
            'WORK_OF_ART': 'WORK_OF_ART',
            'LAW': 'LAW',
            'LANGUAGE': 'LANGUAGE',
            'DATE': 'DATE',
            'TIME': 'TIME',
            'PERCENT': 'PERCENT',
            'MONEY': 'MONEY',
            'QUANTITY': 'QUANTITY',
            'ORDINAL': 'ORDINAL',
            'CARDINAL': 'CARDINAL',
        }
        
        # Store mappings for de-anonymization
        self.alias_mapping = {}
        self.reverse_mapping = {}
    
    def _generate_alias(self, original_value: str, data_type: str) -> str:
        """Generate a consistent alias for a value"""
        # Create a hash of the original value for consistency
        hash_object = hashlib.md5(original_value.encode())
        hash_hex = hash_object.hexdigest()[:8]
        return f"[{data_type}_{hash_hex}]"
    
    def anonymize_text(self, text: str) -> Tuple[str, Dict[str, str]]:
        """
        Anonymize sensitive data in text using spaCy NER
        
        Returns:
            Tuple of (anonymized_text, mapping_of_original_to_alias)
        """
        if not text:
            return text, {}
        
        print(f"🔍 Starting spaCy anonymization of text ({len(text)} characters)")
        anonymized_text = text
        all_mappings = {}
        
        # Process structured patterns first (emails, phones, etc.)
        print(f"🔍 Processing structured patterns...")
        for data_type, pattern in self.patterns.items():
            matches = re.finditer(pattern, anonymized_text)
            for match in matches:
                original_value = match.group()
                alias = self._generate_alias(original_value, data_type)
                all_mappings[original_value] = alias
                print(f"   Found {data_type}: '{original_value}' → '{alias}'")
                anonymized_text = re.sub(re.escape(original_value), alias, anonymized_text)
        
        # Process spaCy entities
        print(f"🔍 Processing spaCy entities...")
        doc = self.nlp(anonymized_text)
        
        # Sort entities by start position (descending) to avoid position shifts
        entities = sorted(doc.ents, key=lambda x: x.start_char, reverse=True)
        
        for ent in entities:
            if ent.label_ in self.entity_types:
                original_value = ent.text
                data_type = self.entity_types[ent.label_]
                alias = self._generate_alias(original_value, data_type)
                
                # Only add if not already processed
                if original_value not in all_mappings:
                    all_mappings[original_value] = alias
                    print(f"   Found {data_type} ({ent.label_}): '{original_value}' → '{alias}'")
                    
                    # Replace in text (from end to start to avoid position shifts)
                    anonymized_text = (
                        anonymized_text[:ent.start_char] + 
                        alias + 
                        anonymized_text[ent.end_char:]
                    )
        
        # Store mappings for potential de-anonymization later
        self.alias_mapping.update(all_mappings)
        self.reverse_mapping.update({v: k for k, v in all_mappings.items()})
        
        print(f"🔍 Total anonymized items: {len(all_mappings)}")
        logger.info(f"spaCy anonymized {len(all_mappings)} sensitive data points")
        return anonymized_text, all_mappings
    
    def deanonymize_text(self, text: str) -> str:
        """Restore original values from aliases"""
        if not text:
            return text
        
        deanonymized_text = text
        for alias, original in self.reverse_mapping.items():
            deanonymized_text = deanonymized_text.replace(alias, original)
        
        return deanonymized_text
    
    def anonymize_question(self, question: str, all_mappings: Dict[str, str]) -> str:
        """
        Anonymize a question using mappings from all uploaded documents
        
        Args:
            question: The user's question
            all_mappings: Combined mappings from all documents
            
        Returns:
            Anonymized question
        """
        if not question or not all_mappings:
            return question
        
        print(f"🔒 Anonymizing question: '{question}'")
        anonymized_question = question
        
        # Create a more flexible mapping that includes partial matches
        flexible_mappings = {}
        for original, alias in all_mappings.items():
            # Add the full original as-is
            flexible_mappings[original] = alias
            
            # For names, also add individual words
            if 'NAME' in alias:
                words = original.split()
                if len(words) > 1:
                    for word in words:
                        if len(word) > 2:  # Only add words longer than 2 chars
                            flexible_mappings[word] = alias
        
        # Replace real names/values with their anonymized versions
        for original, alias in flexible_mappings.items():
            # Use case-insensitive replacement for better matching
            pattern = re.compile(re.escape(original), re.IGNORECASE)
            anonymized_question = pattern.sub(alias, anonymized_question)
        
        print(f"🔒 Anonymized question: '{anonymized_question}'")
        return anonymized_question
    
    def deanonymize_answer(self, answer: str, all_mappings: Dict[str, str]) -> str:
        """
        Deanonymize an AI answer using mappings from all uploaded documents
        
        Args:
            answer: The AI's answer
            all_mappings: Combined mappings from all documents
            
        Returns:
            Deanonymized answer
        """
        if not answer or not all_mappings:
            return answer
        
        print(f"🔓 Deanonymizing answer (first 100 chars): '{answer[:100]}...'")
        deanonymized_answer = answer
        
        # Replace anonymized versions with original values
        for original, alias in all_mappings.items():
            deanonymized_answer = deanonymized_answer.replace(alias, original)
        
        print(f"🔓 Deanonymized answer (first 100 chars): '{deanonymized_answer[:100]}...'")
        return deanonymized_answer
    
    def get_mapping_summary(self) -> Dict[str, int]:
        """Get a summary of anonymized data types"""
        summary = {}
        for original, alias in self.alias_mapping.items():
            # Extract data type from alias [TYPE_hash]
            if alias.startswith('[') and ']' in alias:
                data_type = alias[1:alias.find('_')]
                summary[data_type] = summary.get(data_type, 0) + 1
        return summary
    
    def clear_mappings(self):
        """Clear stored mappings"""
        self.alias_mapping.clear()
        self.reverse_mapping.clear()
        print("🧹 Cleared anonymization mappings") 