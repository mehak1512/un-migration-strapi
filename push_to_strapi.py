# push_to_strapi.py
import requests

STRAPI_URL = "http://localhost:1337/api/pages"
STRAPI_TOKEN = "YOUR_STRAPI_API_TOKEN"

def push_to_strapi(data):
    headers = {
        "Authorization": f"Bearer {STRAPI_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {"data": data}
    res = requests.post(STRAPI_URL, headers=headers, json=payload)

    if res.status_code == 200 or res.status_code == 201:
        print("✅ Uploaded successfully:", data.get("title", ""))
    else:
        print("❌ Failed:", res.text)
