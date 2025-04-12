# models/schemas.py
from pydantic import BaseModel
from typing import List, Optional

class Experience(BaseModel):
    company: Optional[str]
    position: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]

class ParsedCV(BaseModel):
    name: Optional[str]
    email: Optional[str]
    skills: List[str]
    experience: List[Experience]
