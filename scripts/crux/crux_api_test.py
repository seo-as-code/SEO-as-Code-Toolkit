import json
import os
import sys

import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))

from lib.site_config import site_origin  # noqa: E402

KEY_FILE = os.path.join(os.path.dirname(__file__), "crux_key.txt")

with open(KEY_FILE, "r", encoding="utf-8") as f:
    API_KEY = f.read().strip()

URL = f"https://chromeuxreport.googleapis.com/v1/records:queryRecord?key={API_KEY}"

payload = {
    "origin": site_origin(),
    "metrics": [
        "largest_contentful_paint",
        "cumulative_layout_shift",
        "interaction_to_next_paint",
    ],
}

response = requests.post(URL, json=payload)
data = response.json()
print(json.dumps(data, indent=2))
