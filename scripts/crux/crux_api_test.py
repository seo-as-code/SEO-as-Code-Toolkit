import requests
import json

# Leer tu API Key desde archivo
with open("crux_key.txt", "r") as f:
    API_KEY = f.read().strip()

URL = f"https://chromeuxreport.googleapis.com/v1/records:queryRecord?key={API_KEY}"

payload = {
    "origin": "https://studiorethinkibiza.com",
    "metrics": [
        "largest_contentful_paint",
        "cumulative_layout_shift",
        "interaction_to_next_paint"
    ]
}

response = requests.post(URL, json=payload)
data = response.json()

print(json.dumps(data, indent=2))
