#!/usr/bin/env python3
"""
Test script to demonstrate and improve name detection
"""

import sys
import os

from backend.services.spacy_anonymizer import SpacyAnonymizer
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

import re

def test_name_detection():
    print("🔍 Name Detection Test")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        "Florentine worked on the project",
        "John Smith is the manager",
        "Dr. Sarah Johnson PhD",
        "Mary-Jane Watson",
        "The project was completed by Alice and Bob",
        "This is not a name",
        "The company hired Max",
        "Anna Maria Schmidt",
        "Prof. Dr. Hans Mueller",
        "The team includes: Alex, Chris, and Dana"
    ]
    
    anonymizer = SpacyAnonymizer()
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: '{text}'")
        
        # Test current patterns
        found_names = []
        for pattern in anonymizer.name_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                name = match.group()
                if not anonymizer._is_common_word(name):
                    found_names.append(name)
        
        if found_names:
            print(f"   ✅ Found names: {found_names}")
        else:
            print(f"   ❌ No names detected")
    
    print(f"\n📊 Current Name Patterns:")
    for i, pattern in enumerate(anonymizer.name_patterns, 1):
        print(f"   {i}. {pattern}")
    
    print(f"\n🔧 Suggestions for improvement:")
    print("   1. Add German name patterns (von, zu, etc.)")
    print("   2. Add title patterns (Dr., Prof., etc.)")
    print("   3. Add list patterns (Alex, Chris, and Dana)")
    print("   4. Add context-based detection")
    print("   5. Use NLP libraries for better accuracy")

if __name__ == "__main__":
    test_name_detection() 