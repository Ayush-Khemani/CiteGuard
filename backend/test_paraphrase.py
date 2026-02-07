#!/usr/bin/env python
"""Test paraphrasing endpoint"""
import requests
import json

API_URL = "http://localhost:8000/api/v1/analysis"

# Test text
test_text = "The cat is sitting on the mat because it is tired. The dog is running around the yard very quickly. This is important work that needs to be done."

print("=" * 60)
print("TESTING PARAPHRASING SERVICE")
print("=" * 60)

styles = ["simple", "academic", "formal", "casual"]

for style in styles:
    print(f"\n📝 Style: {style.upper()}")
    print("-" * 60)
    
    payload = {
        "text": test_text,
        "context": style
    }
    
    try:
        response = requests.post(
            f"{API_URL}/paraphrase",
            json=payload,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"\n📌 Original:\n{test_text}")
            print(f"\n✨ Paraphrased:\n{data['paraphrased_text']}")
            print(f"\n🔧 Method: {data.get('method', 'unknown')}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
    
    except Exception as e:
        print(f"❌ Exception: {e}")

print("\n" + "=" * 60)
