import os
import io
import base64
from PIL import Image
import pdfplumber
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# Load OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Initialize the ChatOpenAI model
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    openai_api_key=openai_api_key
)

SYSTEM_MESSAGE = """
You are EcoBot, an AI-powered ecological assistant. Your goal is to help users identify species from images or text,
answer biodiversity-related questions, and provide scientifically accurate information.
Use scientific reasoning and reliable sources where applicable.
If unsure, acknowledge the uncertainty rather than making up an answer.
"""

def process_with_gpt4o(query: str, history: list, file_content: bytes = None, file_type: str = None) -> dict:
    """Generate a response from GPT-4o Mini, handling text, images, PDFs, and chat history."""
    
    messages = [SystemMessage(content=SYSTEM_MESSAGE)]

    # Add chat history for context
    for entry in history:
        if entry["role"] == "user":
            messages.append(HumanMessage(content=entry["content"]))
        else:
            messages.append(AIMessage(content=entry["content"]))

    # Handle image or PDF attachments
    if file_content:
        if "image" in file_type:
            try:
                # Encode image to base64
                image_b64 = base64.b64encode(file_content).decode()
                messages.append(HumanMessage(content=query, additional_kwargs={"image": image_b64}))
            except Exception as e:
                print(f"❌ Error processing image: {str(e)}")
                return {"response": f"Error processing image: {str(e)}"}

        elif "pdf" in file_type:
            try:
                with pdfplumber.open(io.BytesIO(file_content)) as pdf:
                    extracted_text = pdf.pages[0].extract_text() if pdf.pages else ""
                messages.append(HumanMessage(content=f"{query}\n\nExtracted text from PDF:\n{extracted_text}"))
            except Exception as e:
                print(f"❌ Error processing PDF: {str(e)}")
                return {"response": f"Error processing PDF: {str(e)}"}

    else:
        messages.append(HumanMessage(content=query))

    # Log messages before calling GPT-4o Mini
    print("📨 Sending messages to GPT-4o Mini:", messages)

    # Generate response using LangChain's ChatOpenAI
    try:
        response = llm.invoke(messages)
        return {"response": response.content}
    except Exception as e:
        print(f"❌ Error calling GPT-4o Mini: {str(e)}")
        return {"response": f"Error calling GPT-4o Mini: {str(e)}"}
