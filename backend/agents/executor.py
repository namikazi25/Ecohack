import sys
import os

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.tools.image_tools import process_image_with_gpt4o
from backend.gpt_handler import process_with_gpt4o
from backend.tools.wiki_tool import fetch_wikipedia_summary
from backend.tools.pdf_tools import process_pdf_with_gpt4o

class ExecutingAgent:
    """Executes the validated plan and retrieves results."""

    def execute(self, plan, history=None):  # ✅ Added history as an optional parameter
        """Executes the validated plan based on the tool selection while keeping track of history."""
        history = history or []  # Initialize if None

        tool = plan.get("tool")
        data = plan.get("data")
        file_type = plan.get("file_type", None)  # ✅ Extract file_type if available

        # **Execution Strategy**
        if tool == "gpt":
            response = process_with_gpt4o(data)  # Calls GPT for general queries
        elif tool == "image":
            if file_type:  # ✅ Ensure we pass file_type for images
                response = process_image_with_gpt4o(data, file_type)
            else:
                return {"error": "File type missing for image processing"}
        elif tool == "pdf":
            extracted_text = data.get("extracted_text")
            user_query = data.get("user_query", "Summarize this document.")
            response = process_pdf_with_gpt4o(extracted_text, user_query)
        elif tool == "wiki":
            response = fetch_wikipedia_summary(data)  # Wikipedia lookup
        else:
            return {"error": "❌ Unknown tool selected."}

        # **Update Chat History**
        history.append({"role": "assistant", "content": response})
        
        return {"response": response, "history": history}  # ✅ Include history in response



