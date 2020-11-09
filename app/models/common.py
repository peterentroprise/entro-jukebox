from pydantic import BaseModel, Field
from enum import Enum

class ModelName(str, Enum):
    oneb_lyrics = "1b_lyrics"
    fiveb_lyrics = "5b_lyrics"
    test = "test"

class GenerateRequest(BaseModel):
      model: ModelName
      sample_length_in_seconds: int = Field(default=20, example=20)
      artist: str = Field(default="Katy Perry", example="Katy Perry")
      genre: str = Field(default="Pop", example="Pop")
      lyrics: str = Field(default="Dueling sails, timelessly quilt the cosmic skies. A tale of reflection and growing, through recursion and glowing. Bound together, woven light forever.", example="Dueling sails, timelessly quilt the cosmic skies. A tale of reflection and growing, through recursion and glowing. Bound together, woven light forever.")