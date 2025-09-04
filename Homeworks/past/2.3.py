from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
import re

app = FastAPI()


class Contact(BaseModel):
    email: EmailStr = Field(..., description="Email address (required)")
    phone: Optional[str] = Field(None, description="Phone number (optional, 7-15 digits)")

    @validator('phone')
    def validate_phone(cls, v):
        if v is None:
            return v
        if not re.match(r'^\d{7,15}$', v):
            raise ValueError('Phone number must contain only digits and be 7-15 characters long')
        return v


class Feedback(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Name (2-50 characters)")
    message: str = Field(..., min_length=10, max_length=500, description="Message (10-500 characters)")
    contact: Contact

    @validator('message')
    def validate_message(cls, v):
        prohibited_words = ["spam", "scam", "fraud"]
        message_lower = v.lower()
        for word in prohibited_words:
            if word in message_lower:
                raise ValueError(f'Message contains prohibited word: {word}')
        return v


@app.post("/feedback")
async def submit_feedback(feedback: Feedback, is_premium: bool = Query(False)):
    base_message = f"Thank you, {feedback.name}! Your review is saved."

    if is_premium:
        priority_message = " Your review will be considered in priority."
        response_message = base_message + priority_message
    else:
        response_message = base_message

    return {"message": response_message}

