from pydantic import BaseModel

class ProcessEmailRequest(BaseModel):
    text: str

class ProcessEmailResponse(BaseModel):
    category: str
    confidence: float
    suggested_reply: str
    classify_source: str
