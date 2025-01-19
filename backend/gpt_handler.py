import os
import io
import base64
from PIL import Image
import pdfplumber
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage

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

def process_with_gpt4o(query: str, file_content: bytes = None, file_type: str = None) -> dict:
    """Generate a response from GPT-4o Mini, handling text, images, and PDFs."""
    user_message = f"User's question: {query}\n"

    if file_content:
        if "image" in file_type:
            # Encode image to base64
            image_b64 = base64.b64encode(file_content).decode()
            user_message += "Attached image: [Processing Image]\n"
            messages = [
                SystemMessage(content=SYSTEM_MESSAGE),
                HumanMessage(content=user_message, additional_kwargs={"image": image_b64}),
            ]
        elif "pdf" in file_type:
            with pdfplumber.open(io.BytesIO(file_content)) as pdf:
                extracted_text = pdf.pages[0].extract_text() if pdf.pages else ""
                user_message += f"Extracted text from PDF:\n{extracted_text}\n"
            messages = [
                SystemMessage(content=SYSTEM_MESSAGE),
                HumanMessage(content=user_message),
            ]
    else:
        messages = [
            SystemMessage(content=SYSTEM_MESSAGE),
            HumanMessage(content=user_message),
        ]

    # Generate response using LangChain's ChatOpenAI
    response = llm.invoke(messages)

    return {"response": response.content}
