import os
from openai import OpenAI

# Load OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("❌ Missing OpenAI API Key. Set OPENAI_API_KEY in your environment variables.")

# Initialize OpenAI Client
client = OpenAI(api_key=OPENAI_API_KEY)
