#!/usr/bin/env python3
"""
Test script to demonstrate privacy mode functionality
"""

import requests


# Test data with sensitive information
test_content = """
Dear John Smith,

Thank you for your application. Here are your details:
- Email: john.smith@example.com
- Phone: +1-555-123-4567
- Address: 123 Main Street, New York, NY 10001
- SSN: 123-45-6789

Please contact us at hr@company.com if you have any questions.

Best regards,
Sarah Johnson
HR Manager
sarah.johnson@company.com
"""

# Create a test file
with open('test_document.txt', 'w') as f:
    f.write(test_content)

print("🔒 Privacy Mode Test")
print("=" * 50)

# Test 1: Upload without privacy mode
print("\n1️⃣ Uploading WITHOUT privacy mode...")
with open('test_document.txt', 'rb') as f:
    files = {'file': ('test_document.txt', f, 'text/plain')}
    data = {'anonymize': 'false'}
    response = requests.post('http://localhost:8000/ingest', files=files, data=data)

if response.status_code == 200:
    result = response.json()
    print(f"✅ Success: {result['message']}")
    print(f"📊 Chunks processed: {result['chunks_processed']}")
    print(f"🔒 Anonymized: {result['anonymized']}")
else:
    print(f"❌ Error: {response.text}")

# Test 2: Upload with privacy mode
print("\n2️⃣ Uploading WITH privacy mode...")
with open('test_document.txt', 'rb') as f:
    files = {'file': ('test_document_private.txt', f, 'text/plain')}
    data = {'anonymize': 'true'}
    response = requests.post('http://localhost:8000/ingest', files=files, data=data)

if response.status_code == 200:
    result = response.json()
    print(f"✅ Success: {result['message']}")
    print(f"📊 Chunks processed: {result['chunks_processed']}")
    print(f"🔒 Anonymized: {result['anonymized']}")
    if result.get('anonymization_summary'):
        print(f"📈 Anonymization summary: {result['anonymization_summary']}")
else:
    print(f"❌ Error: {response.text}")

# Test 3: Check files list
print("\n3️⃣ Checking files list...")
response = requests.get('http://localhost:8000/files')
if response.status_code == 200:
    files = response.json()['files']
    print(f"📁 Found {len(files)} files:")
    for file in files:
        privacy_status = "🔒 Protected" if file['anonymized'] else "📄 Standard"
        print(f"   - {file['filename']}: {privacy_status}")
else:
    print(f"❌ Error: {response.text}")

print("\n🎉 Privacy mode test completed!") 