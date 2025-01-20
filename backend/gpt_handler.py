import os
import io
import base64
import pdfplumber
from dotenv import load_dotenv
from openai import OpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

# Load OpenAI API key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("❌ OPENAI_API_KEY environment variable is not set.")

# Initialize OpenAI client (for image handling)
client = OpenAI(api_key=openai_api_key)

# Initialize LangChain for text & PDFs
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    openai_api_key=openai_api_key
)

# System message for GPT-4o
SYSTEM_MESSAGE = SystemMessage(
    content="""You are EcoBot, an AI-powered ecological assistant. Your goal is to help users identify species from images or text,
    answer biodiversity-related questions, and provide scientifically accurate information.
    Use scientific reasoning and reliable sources where applicable.
    If unsure, acknowledge the uncertainty rather than making up an answer."""
)

def extract_text_from_pdf(file_content: bytes) -> str:
    """Extracts text from a PDF file."""
    try:
        with pdfplumber.open(io.BytesIO(file_content)) as pdf:
            extracted_text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        return extracted_text.strip() if extracted_text else "No readable text found in the PDF."
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"

def encode_image(file_content: bytes, file_type: str) -> str:
    """Encodes an image to Base64 format for GPT-4o processing."""
    try:
        base64_encoded = base64.b64encode(file_content).decode("utf-8")
        return f"data:image/{file_type.split('/')[-1]};base64,{base64_encoded}"
    except Exception as e:
        return None

def process_image_with_gpt4o(image_data_url: str, query: str = "Identify this species.") -> str:
    """Sends an image to GPT-4o for species identification."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": query},
                        {"type": "image_url", "image_url": {"url": image_data_url, "detail": "high"}},
                    ],
                }
            ],
            max_tokens=500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error calling GPT-4o: {str(e)}"

def process_with_gpt4o(query: str, history: list, file_content: bytes = None, file_type: str = None) -> dict:
    """Handles text, images, and PDFs for GPT-4o processing."""

    messages = [SYSTEM_MESSAGE]

    # Add chat history for context
    for entry in history:
        if entry["role"] == "user":
            messages.append(HumanMessage(content=[{"type": "text", "text": entry["content"]}]))
        else:
            messages.append(AIMessage(content=entry["content"]))  # Add AI responses as well

    # Handle Image Processing
    if file_content and file_type and "image" in file_type:
        image_data_url = encode_image(file_content, file_type)
        if not image_data_url:
            return {"response": "Error encoding image."}
        
        image_response = process_image_with_gpt4o(image_data_url, query)

        # **Fix: Append Image Response to Message History**
        messages.append(AIMessage(content=image_response))
        return {"response": image_response}

    # Handle PDFs
    elif file_content and file_type and "pdf" in file_type:
        extracted_text = extract_text_from_pdf(file_content)
        query = f"{query}\n\nExtracted text from PDF:\n{extracted_text}"

    messages.append(HumanMessage(content=[{"type": "text", "text": query}]))

    try:
        response = llm.invoke(messages)
        bot_response = response.content

        # **Fix: Append Text/PDF Response to Message History**
        messages.append(AIMessage(content=bot_response))
        return {"response": bot_response}
    except Exception as e:
        return {"response": f"❌ Error calling GPT-4o: {str(e)}"}
