from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from gpt_handler import process_with_gpt4o
import io

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/query/")
async def process_query(query: str = Form(...), file: UploadFile = File(None)):
    file_content = await file.read() if file else None
    file_type = file.content_type if file else None
    
    response = process_with_gpt4o(query, file_content, file_type)
    
    return response
