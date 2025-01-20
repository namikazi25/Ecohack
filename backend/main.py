from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from gpt_handler import process_with_gpt4o
import json

app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    history: list  # Chat history

@app.post("/query/")
async def process_query(
    query: str = Form(...),
    history: str = Form("[]"),  
    file: UploadFile = File(None)
):
    file_content = None
    file_type = None

    if file:
        file_content = await file.read()
        file_type = file.content_type

    # Convert history from JSON string to list
    try:
        history = json.loads(history)
    except json.JSONDecodeError:
        history = []

    response = process_with_gpt4o(query, history, file_content, file_type)

    return response
