import sys
import os
import re

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.gpt_handler import generate_plan_with_gpt4o
from backend.tools.image_tools import process_image_with_gpt4o
from backend.tools.pdf_tools import extract_text_from_pdf

class PlanningAgent:
    """Generates execution plans using GPT-4o and domain-specific heuristics"""
    
    WIKI_TRIGGERS = [
        "wikipedia", "verified source", "scientific name", "taxonomy of",
        "habitat of", "conservation status", "according to", "peer-reviewed",
        "scientific consensus", "academic sources", "species classification",
        "kingdom", "phylum", "genus", "family"
    ]
    
    FULL_PAGE_KEYWORDS = [
        "full article", "complete page", "detailed study", 
        "entire entry", "full text"
    ]

    def plan(self, query, file_content=None, file_type=None, history=None):
        """Generate execution plan considering multiple data sources"""
        history = history or []
        plan = {"tool": "gpt", "data": query}  # Default plan

        try:
            # Prioritize file-based operations
            if file_content:
                plan = self._handle_file_content(query, file_content, file_type)
            
            # Wikipedia detection takes precedence over GPT
            elif self._requires_wikipedia(query):
                plan = self._create_wiki_plan(query)
            
            # Fallback to GPT with context
            else:
                plan = self._create_gpt_plan(query, history)

        except Exception as e:
            plan = self._create_error_plan(f"Planning error: {str(e)}")

        return plan

    def _handle_file_content(self, query, file_content, file_type):
        """Process files with validation and error handling"""
        if "image" in file_type:
            return {
                "tool": "image",
                "data": file_content,
                "file_type": file_type,
                "rationale": "Image file uploaded for analysis"
            }
            
        if "pdf" in file_type:
            if not isinstance(file_content, bytes):
                raise ValueError("PDF content must be bytes")
                
            extracted_text = extract_text_from_pdf(file_content)
            if "❌" in extracted_text:
                raise ValueError(extracted_text)
                
            return {
                "tool": "pdf",
                "data": {
                    "extracted_text": extracted_text,
                    "user_query": query
                },
                "rationale": "PDF document processing"
            }
        
        raise ValueError("Unsupported file type")

    def _create_wiki_plan(self, query):
        """Create Wikipedia-specific execution plan"""
        clean_query = self._clean_wiki_query(query)
        needs_full = self._needs_full_page(query)
        
        return {
            "tool": "wiki_full" if needs_full else "wiki",
            "data": clean_query,
            "rationale": f"Wikipedia {'full page' if needs_full else 'summary'} request for: {clean_query}"
        }

    def _create_gpt_plan(self, query, history):
        """Create GPT plan with conversation context"""
        context = self._build_conversation_context(history)
        return {
            "tool": "gpt",
            "data": f"{context}\n\n{query}",
            "rationale": "General ecological query with conversation context"
        }

    def _create_error_plan(self, error_msg):
        return {
            "tool": "gpt",
            "data": error_msg,
            "rationale": "Error handling fallback"
        }

    def _requires_wikipedia(self, query: str) -> bool:
        """Check if query requires Wikipedia verification"""
        query_lower = query.lower()
        return any(trigger in query_lower for trigger in self.WIKI_TRIGGERS)

    def _needs_full_page(self, query: str) -> bool:
        """Determine if full Wikipedia page is needed"""
        return any(kw in query.lower() for kw in self.FULL_PAGE_KEYWORDS)

    def _clean_wiki_query(self, query: str) -> str:
        """Normalize Wikipedia search query"""
        # Remove Wikipedia references and truncate
        clean = re.sub(r'\(?according to wikipedia\)?', '', query, flags=re.IGNORECASE)
        clean = re.sub(r'\bwikipedia\b', '', clean, flags=re.IGNORECASE)
        return clean.strip()[:150]  # Limit to 150 characters

    def _build_conversation_context(self, history):
        """Build context from last 3 messages"""
        return "\n".join(
            f"{msg['role']}: {msg['content']}" 
            for msg in history[-3:]
        )