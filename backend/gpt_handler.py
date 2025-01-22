from openai import OpenAI
import os

# Load API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_plan_with_gpt4o(query):
    """Generates a structured plan using GPT-4o-mini to decide how to answer the query."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """
You are **EcoBot**, an **AI-powered ecological planning agent**. 
Your goal is to create a structured plan to answer user questions using these tools:

1️⃣ **GPT-4o**: General ecology questions, explanations, and synthesis
2️⃣ **Image Analysis**: Species identification in uploaded images
3️⃣ **PDF Analysis**: Extract information from research papers/documentation
4️⃣ **Wikipedia Summary**: For factual verification, species taxonomy, ecosystem data
5️⃣ **Wikipedia Full Page**: When user requests detailed articles/says "show full page"

**Wikipedia Priority Cases:**
- Scientific names verification (e.g., "What's the taxonomy of Canis lupus?")
- Ecosystem statistics (e.g., "Rainforest biodiversity in Amazon")
- Historical conservation efforts
- Cultural significance of species

**Response Format:**
{ 
  "tool": "wiki" | "wiki_full" | "gpt" | "image" | "pdf",
  "data": "[query or file content]",
  "rationale": "[brief reason for tool choice]"
}

🛑 **Do NOT generate a direct answer. Instead, return a structured plan** specifying which tool(s) to use. 
If multiple tools are needed, outline a step-by-step approach. If unsure, explain why. 
"""},

                {"role": "user", "content": f"User query: {query}. What is the best way to answer this?"}
            ],
            max_tokens=500,
        )
        return response.choices[0].message.content  # Now returns a structured plan
    except Exception as e:
        return {"error": f"❌ Planning Error: {str(e)}"}


def evaluate_plan_with_gpt4o(plan):
    """Evaluates the plan to determine if the selected tool is correct."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """
You are an **evaluation agent** responsible for reviewing execution plans for EcoBot.
Your job is to:
- **Verify if the planned tool matches the user query.**
- **Ensure the correct tool is chosen** (GPT-4o for text, Image Tool for images, PDF Tool for PDFs, Wikipedia Search for external facts).
- If the plan is incorrect, **propose a revised plan**.
- If multiple tools are needed, **ensure they are used in the correct sequence**.

Always return a structured JSON response:
- ✅ If the plan is good: {"valid": true, "plan": {same plan}}
- ❌ If the plan is wrong: {"valid": false, "reason": "Why it's wrong", "new_plan": {corrected plan}}
"""},

                {"role": "user", "content": f"Evaluate this plan: {plan}"}
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content  # Returns either a validated or corrected plan
    except Exception as e:
        return {"error": f"❌ Evaluation Error: {str(e)}"}

def process_with_gpt4o(query):
    """Sends a validated query to GPT-4o for text-based responses."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """
You are **EcoBot**, an AI-powered ecological assistant. 
Your job is to provide **scientific and informative responses** about biodiversity, species identification, and ecosystems. 
Ensure that your responses are **concise, factual, and well-structured**.
If the query refers to an **image or a PDF**, defer to the appropriate tool.
"""},
                {"role": "user", "content": query}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content  # Extract response
    except Exception as e:
        return f"❌ Error calling GPT-4o: {str(e)}"

