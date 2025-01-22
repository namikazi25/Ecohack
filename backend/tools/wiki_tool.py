import requests
import json

WIKIPEDIA_API_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/"

def fetch_wikipedia_summary(query: str) -> str:
    """Fetches a short summary from Wikipedia."""
    try:
        response = requests.get(f"{WIKIPEDIA_API_URL}{query.replace(' ', '_')}")
        if response.status_code == 200:
            data = response.json()
            return data.get("extract", "No summary available.")
        return f"❌ Wikipedia API Error: {response.status_code}"
    except Exception as e:
        return f"❌ Wikipedia fetch error: {str(e)}"
