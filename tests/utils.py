import os
from pathlib import Path
TEST_DIR = Path(__file__).parent

class JsonUtils:
    json_base = {
        "active": True,
        "description": "",
        "update_by": "admin",
        "url": "https://www.google.com/",
        "url_preview_image": "https://www.google.com/"
    }
    
    header = {
        'Content-Type': 'application/json', 
        'Authorization': 'Bearer ' + os.getenv("API_TOKEN")
    }
    
    @staticmethod
    def get_json_feature_extract_model():
        return {
            "fullPath": str(TEST_DIR / "test.jpeg")
        }