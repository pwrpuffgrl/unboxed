#!/usr/bin/env python3
"""
Test script to verify two-way anonymization functionality
"""

import requests

# Test data with a specific person's name
test_content = """
Florentine worked on the Unboxed project.
She developed the privacy features and implemented the anonymization system.
Florentine's email is florentine@example.com and her phone is +1-555-123-4567.
The project was completed by Florentine and her team.
"""

print("🔒 Two-Way Anonymization Test")
print("=" * 50)

# Step 1: Upload document with privacy mode enabled
print("\n1️⃣ Uploading document with privacy mode...")
with open('florentine_doc.txt', 'w') as f:
    f.write(test_content)

with open('florentine_doc.txt', 'rb') as f:
    files = {'file': ('florentine_doc.txt', f, 'text/plain')}
    data = {'anonymize': 'true'}
    response = requests.post('http://localhost:8000/ingest', files=files, data=data)

if response.status_code == 200:
    result = response.json()
    print(f"✅ Document uploaded successfully")
    print(f"🔒 Anonymized: {result['anonymized']}")
    if result.get('anonymization_summary'):
        print(f"📊 Anonymization summary: {result['anonymization_summary']}")
else:
    print(f"❌ Upload failed: {response.text}")
    exit(1)

# Step 2: Test question anonymization
print("\n2️⃣ Testing question anonymization...")
questions = [
    "What project did Florentine work on?",
    "What is Florentine's email?",
    "Who completed the project?",
    "What are Florentine's contact details?"
]

for question in questions:
    print(f"\n   Question: '{question}'")
    response = requests.post('http://localhost:8000/ask', 
                           json={'question': question, 'context_limit': 5})
    
    if response.status_code == 200:
        result = response.json()
        print(f"   Answer: {result['answer']}")
        print(f"   Confidence: {result['confidence']:.2f}")
        if result['sources']:
            print(f"   Sources: {result['sources']}")
    else:
        print(f"   ❌ Error: {response.text}")

# Step 3: Test with non-personal questions
print("\n3️⃣ Testing with general questions...")
general_questions = [
    "What is the project about?",
    "What features were developed?",
    "What is the main topic?"
]

for question in general_questions:
    print(f"\n   Question: '{question}'")
    response = requests.post('http://localhost:8000/ask', 
                           json={'question': question, 'context_limit': 5})
    
    if response.status_code == 200:
        result = response.json()
        print(f"   Answer: {result['answer']}")
        print(f"   Confidence: {result['confidence']:.2f}")
    else:
        print(f"   ❌ Error: {response.text}")

print("\n🎉 Two-way anonymization test completed!")
print("\n💡 The system should now:")
print("   - Anonymize questions containing real names")
print("   - Find relevant content using anonymized data")
print("   - Deanonymize answers to show real names to users") 