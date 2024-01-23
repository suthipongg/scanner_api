from pydantic import BaseModel, Field
from models.utils import ManageBody

class ExtractModel(BaseModel, ManageBody):
    image_path : str = Field(..., description="Image Path (**required)")
    
    def __init__(self, **data):
        super().__init__(**data)
        self.clean_model(keys_require=['image_path'])
    
    class Config:
        json_schema_extra = {
            "example": {
                "image_path": "https://uat-chat.cosmenet.in.th/1.jpeg"
            }
        }