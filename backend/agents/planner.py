import sys
import os

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.gpt_handler import generate_plan_with_gpt4o
from backend.tools.image_tools import process_image_with_gpt4o  # ✅ Use correct function
from backend.tools.pdf_tools import extract_text_from_pdf

class PlanningAgent:
    """Uses GPT-4o-mini to generate structured plans for query execution."""

    def plan(self, query, file_content=None, file_type=None, history=None):
        """Uses history for better planning."""
        history = history or []  # Default to empty list if None

        if file_content:
            if "image" in file_type:
                return {"tool": "image", "data": file_content, "file_type": file_type}  # ✅ Correct function
            elif "pdf" in file_type:
                if not isinstance(file_content, bytes):
                    return {"error": "❌ PDF content must be bytes."}
                extracted_text = extract_text_from_pdf(file_content)
                if "❌" in extracted_text:
                    return {"error": extracted_text}
                return {"tool": "pdf", "data": {"extracted_text": extracted_text, "user_query": query}}

        # **Consider past interactions when planning**
        context_query = "\n".join([msg["content"] for msg in history[-3:]])  # Use last 3 messages for context

        return {"tool": "gpt", "data": f"{context_query}\n\n{query}"}
