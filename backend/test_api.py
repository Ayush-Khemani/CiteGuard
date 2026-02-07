import requests
import json

api_url = 'http://localhost:8000/api/v1/analysis/analyze'
test_text = 'This is a sample text for testing the plagiarism detection system'

print("Testing Plagiarism Analysis Endpoint...")
print(f"URL: {api_url}")
print(f"Payload: {{'text': '{test_text}', 'threshold': 0.7}}\n")

try:
    response = requests.post(api_url, json={'text': test_text, 'threshold': 0.7}, timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*60 + "\n")

# Test citation endpoint
api_url = 'http://localhost:8000/api/v1/analysis/citation'
data = {
    'title': 'Deep Learning for NLP',
    'authors': ['Yoshua Bengio', 'Yann LeCun'],
    'year': 2024,
    'citation_style': 'APA'
}

print("Testing Citation Generation Endpoint...")
print(f"URL: {api_url}")
print(f"Payload: {json.dumps(data, indent=2)}\n")

try:
    response = requests.post(api_url, json=data, timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
