
import requests
import json

url = "https://safespeak-zoec.onrender.com/analyze"
payload = {
    "message": "You are stupid",
    "user_id": "test_script"
}

print(f"Testing Production URL: {url}")
try:
    response = requests.post(url, json=payload, timeout=30)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Response:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error Body: {response.text}")
except Exception as e:
    print(f"Request Failed: {e}")
