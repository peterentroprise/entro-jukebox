from typing import Optional

from fastapi import FastAPI

from app.generate_service import generate_audio, generate_audio_full
from app.models.common import GenerateRequest
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "Universe"}

@app.post("/generate")
async def generate(request: GenerateRequest):
    response = generate_audio(request)
    return response

@app.post("/generate_full")
async def generate_full(request: GenerateRequest):
    response = generate_audio_full(request)
    return response