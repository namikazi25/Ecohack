import requests
from typing import Optional, Dict
import re

WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"
WIKIPEDIA_PAGE_BASE = "https://en.wikipedia.org/wiki"  # <-- ADD THIS LINE


def search_wikipedia(query: str, sentences: int = 3) -> Optional[Dict]:
    """Search Wikipedia and return structured data with page validation."""
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
        "srlimit": 3
    }
    
    try:
        search_response = requests.get(WIKIPEDIA_API, params=params, timeout=10)
        search_data = search_response.json()
        
        if not search_data.get('query', {}).get('search'):
            return None
            
        best_match = search_data['query']['search'][0]
        page_id = best_match['pageid']
        
        # Get full page content
        content_params = {
            "action": "query",
            "prop": "extracts|info",
            "pageids": page_id,
            "exsentences": sentences,
            "explaintext": True,
            "inprop": "url",
            "format": "json"
        }
        
        content_response = requests.get(WIKIPEDIA_API, params=content_params)
        content_data = content_response.json()
        page = content_data['query']['pages'][str(page_id)]
        
        return {
            "title": page['title'],
            "summary": clean_text(page.get('extract', '')),
            "url": page['fullurl'],
            "pageid": page_id
        }
        
    except Exception as e:
        print(f"Wikipedia API Error: {str(e)}")
        return None

def clean_text(text: str) -> str:
    """Clean Wikipedia text for GPT consumption."""
    return re.sub(r'\s+', ' ', text).strip()

def fetch_full_page(pageid: int) -> Optional[str]:
    """Fetch full page content by page ID"""
    try:
        params = {
            "action": "query",
            "prop": "extracts",
            "pageids": pageid,
            "explaintext": True,
            "format": "json"
        }
        response = requests.get(WIKIPEDIA_API, params=params, timeout=15)
        data = response.json()
        return {
            "content": data['query']['pages'][str(pageid)].get('extract', ''),
            "title": data['query']['pages'][str(pageid)]['title']  # Add title
        }
    except Exception as e:
        print(f"Full page fetch error: {str(e)}")
        return None