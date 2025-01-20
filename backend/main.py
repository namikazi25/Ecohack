from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from gpt_handler import process_with_gpt4o
import io
import json  # ✅ Add this

app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    history: list  # Chat history

@app.post("/query/")
async def process_query(
    query: str = Form(...),
    history: str = Form("[]"),  # ✅ History is received as a string
    file: UploadFile = File(None)
):
    file_content = await file.read() if file else None
    file_type = file.content_type if file else None

    # ✅ Convert `history` from JSON string to Python list
    try:
        history = json.loads(history)  # Convert JSON string to list
    except json.JSONDecodeError:
        history = []  # Default to empty list if parsing fails

    print(f"📩 Received query: {query}")
    print(f"📜 Chat history: {history}")  # ✅ Now correctly parsed as a list
    if file:
        print(f"📄 Uploaded file type: {file_type}, size: {len(file_content)} bytes")

    response = process_with_gpt4o(query, history, file_content, file_type)

    print(f"📨 Response sent: {response}")

    return response
