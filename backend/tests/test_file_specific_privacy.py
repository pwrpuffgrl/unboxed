#!/usr/bin/env python3
"""
Test script to verify file-specific privacy mode functionality
"""

import requests

# Test data with sensitive information
test_content_1 = """
Dear John Smith,
Your email is john.smith@example.com
Phone: +1-555-123-4567
SSN: 123-45-6789
"""

test_content_2 = """
This is a public document.
No sensitive information here.
Just some regular text.
"""

print("🔒 File-Specific Privacy Mode Test")
print("=" * 50)

# Test 1: Upload with privacy mode enabled
print("\n1️⃣ Uploading sensitive document WITH privacy mode...")
with open('sensitive_doc.txt', 'w') as f:
    f.write(test_content_1)

with open('sensitive_doc.txt', 'rb') as f:
    files = {'file': ('sensitive_doc.txt', f, 'text/plain')}
    data = {'anonymize': 'true'}
    response = requests.post('http://localhost:8000/ingest', files=files, data=data)

if response.status_code == 200:
    result = response.json()
    print(f"✅ Success: {result['message']}")
    print(f"🔒 Anonymized: {result['anonymized']}")
    if result.get('anonymization_summary'):
        print(f"📊 Anonymization summary: {result['anonymization_summary']}")
else:
    print(f"❌ Error: {response.text}")

# Test 2: Upload without privacy mode
print("\n2️⃣ Uploading public document WITHOUT privacy mode...")
with open('public_doc.txt', 'w') as f:
    f.write(test_content_2)

with open('public_doc.txt', 'rb') as f:
    files = {'file': ('public_doc.txt', f, 'text/plain')}
    data = {'anonymize': 'false'}
    response = requests.post('http://localhost:8000/ingest', files=files, data=data)

if response.status_code == 200:
    result = response.json()
    print(f"✅ Success: {result['message']}")
    print(f"🔒 Anonymized: {result['anonymized']}")
    if result.get('anonymization_summary'):
        print(f"📊 Anonymization summary: {result['anonymization_summary']}")
else:
    print(f"❌ Error: {response.text}")

# Test 3: Check files list to see different privacy settings
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

print("\n🎉 File-specific privacy mode test completed!")
print("\n💡 In the frontend, users will now see a privacy prompt for each file before upload!") 