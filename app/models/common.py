from pydantic import BaseModel
from enum import Enum

class ModelName(str, Enum):
    oneb_lyrics = "1b_lyrics"
    fiveb_lyrics = "5b_lyrics"
    test = "test"

class GenerateRequest(BaseModel):
      model: ModelName