import requests
from bs4 import BeautifulSoup
import json
import os
from openai import OpenAI


# --- SETUP OPENAI CLIENT ---
# ✅ Place your actual secret key here
os.environ["OPENAI_API_KEY"] = "you api key"
client = OpenAI()


# --- STEP 1: CRAWL THE PAGE ---
def crawl_page(url):
    """Fetch and extract clean text from a webpage."""
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator=" ", strip=True)
        return text[:8000]  # GPT can handle more context
    except Exception as e:
        return f"Error fetching page: {e}"


# --- STEP 2: SUMMARIZE WITH GPT-3.5 ---
def summarize_with_gpt(text, url):
    """Summarize given text using OpenAI GPT-3.5."""
    try:
        prompt = f"""
Summarize the following webpage content clearly and concisely.
Return ONLY valid JSON in this format:
{{
  "url": "{url}",
  "summary": "your summary here"
}}

Text:
{text}
"""
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a precise summarization AI."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,
        )

        content = response.choices[0].message.content.strip()

        # Try to parse the response as JSON
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"url": url, "summary": content}

    except Exception as e:
        return {"url": url, "summary": f"Error: {e}"}


# --- STEP 3: UPLOAD TO STRAPI ---
def upload_to_strapi(data):
    """Send summarized data to Strapi collection."""
    try:
        response = requests.post(
            "http://localhost:1337/api/un-summaries",
            json={"data": data}
        )
        if response.status_code in [200, 201]:
            print("✅ Uploaded successfully to Strapi")
        else:
            print(f"❌ Upload failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error uploading to Strapi: {e}")


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    url = "https://www.un.org/en/about-us"
    text = crawl_page(url)
    summary = summarize_with_gpt(text, url)
    print(summary)
    upload_to_strapi(summary)
