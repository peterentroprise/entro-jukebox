from typing import Optional

from fastapi import FastAPI

from app.generate_service import generate_audio
from app.models.common import GenerateRequest
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "Universe"}

@app.post("/generate")
async def generate(request: GenerateRequest):
    response = generate_audio(request)
    return response