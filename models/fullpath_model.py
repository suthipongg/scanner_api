from pydantic import BaseModel, Field

class FullPathModel(BaseModel):
    fullPath : str = Field(..., description="Image Path (**required)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "fullPath": "https://uat-chat.cosmenet.in.th/1.jpeg"
            }
        }