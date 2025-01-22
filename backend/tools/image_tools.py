import base64
import io
from backend.tools.openai_client import client  # Use shared OpenAI client

def encode_image(file_content: bytes, file_type: str) -> str:
    """Encodes an image to Base64 format for GPT-4o processing."""
    try:
        base64_encoded = base64.b64encode(file_content).decode("utf-8")
        return f"data:image/{file_type.split('/')[-1]};base64,{base64_encoded}"
    except Exception as e:
        return None

def process_image_with_gpt4o(file_content: bytes, file_type: str, query="Identify this species.") -> str:
    """Sends an image to GPT-4o for species identification."""
    image_data_url = encode_image(file_content, file_type)

    if not image_data_url:
        return "❌ Error: Image encoding failed."

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
        return f"❌ Error processing image: {str(e)}"
