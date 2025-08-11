#!/usr/bin/env python3
"""
Test script to verify delete functionality
"""

import requests

# Test data
test_content = """
This is a test document for deletion.
It contains some sample text.
"""

print("🗑️ Delete Functionality Test")
print("=" * 40)

# Step 1: Upload a test file
print("\n1️⃣ Uploading test file...")
with open('test_delete.txt', 'w') as f:
    f.write(test_content)

with open('test_delete.txt', 'rb') as f:
    files = {'file': ('test_delete.txt', f, 'text/plain')}
    data = {'anonymize': 'false'}
    response = requests.post('http://localhost:8000/ingest', files=files, data=data)

if response.status_code == 200:
    result = response.json()
    file_id = result.get('file_id') or 1  # Fallback to ID 1
    print(f"✅ File uploaded successfully")
    print(f"📄 Filename: {result['filename']}")
    print(f"📊 Chunks processed: {result['chunks_processed']}")
else:
    print(f"❌ Upload failed: {response.text}")
    exit(1)

# Step 2: Verify file exists
print(f"\n2️⃣ Verifying file exists (ID: {file_id})...")
response = requests.get('http://localhost:8000/files')
if response.status_code == 200:
    files = response.json()['files']
    file_exists = any(f['id'] == file_id for f in files)
    print(f"📁 File exists: {file_exists}")
    if file_exists:
        print(f"📄 Found {len(files)} files total")
else:
    print(f"❌ Failed to get files: {response.text}")

# Step 3: Delete the file
print(f"\n3️⃣ Deleting file (ID: {file_id})...")
response = requests.delete(f'http://localhost:8000/files/{file_id}')
if response.status_code == 200:
    result = response.json()
    print(f"✅ {result['message']}")
else:
    print(f"❌ Delete failed: {response.text}")

# Step 4: Verify file is deleted
print(f"\n4️⃣ Verifying file is deleted...")
response = requests.get('http://localhost:8000/files')
if response.status_code == 200:
    files = response.json()['files']
    file_exists = any(f['id'] == file_id for f in files)
    print(f"📁 File still exists: {file_exists}")
    print(f"📄 Remaining files: {len(files)}")
else:
    print(f"❌ Failed to get files: {response.text}")

print("\n🎉 Delete functionality test completed!") 