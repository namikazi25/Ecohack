import sys
import os

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.tools.image_tools import process_image_with_gpt4o
from backend.gpt_handler import process_with_gpt4o
from backend.tools.pdf_tools import process_pdf_with_gpt4o
from backend.tools.wiki_tool import search_wikipedia, fetch_full_page

class ExecutingAgent:
    """Executes the validated plan and retrieves results."""

    def execute(self, plan, history=None):  # ✅ Added history as an optional parameter
        """Executes the validated plan based on the tool selection while keeping track of history."""
        history = history or []  # Initialize if None
        response = {"response": "", "sources": []}
        
        tool = plan.get("tool")
        data = plan.get("data")
        file_type = plan.get("file_type", None)  # ✅ Extract file_type if available

        # Initialize default response
        response = {
            "response": "❌ Unable to process request",
            "sources": []
        }

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
                result = search_wikipedia(data)
                if result:
                    response["response"] = f"🌐 **{result['title']}**\n{result['summary']}"
                    response["sources"] = [result['url']]
                else:
                    response["response"] = "❌ No relevant Wikipedia articles found"

        # Add new execution branch
        elif tool == "wiki_full":
            if not data.isdigit():
                return {"error": "Invalid page ID format"}
            full_content = fetch_full_page(int(data))
            if full_content:
                return {
                    "response": f"📚 Full Wikipedia Content:\n{full_content[:3000]}...",
                    "sources": [f"Wikipedia Page ID: {data}"]
                }
            return {"response": "❌ Could not retrieve full article"}
            
        

        # **Update Chat History**
        history.append({"role": "assistant", "content": response})
        
        return {"response": response, "history": history}  # ✅ Include history in response



