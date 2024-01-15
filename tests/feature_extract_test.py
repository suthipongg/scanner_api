from fastapi.testclient import TestClient
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app
from tests.utils import JsonUtils
from dotenv import load_dotenv
load_dotenv()

client = TestClient(app)

def test_feature_extract_success():
    response = client.post("/cosmenet/scanproduct/v2/onnx", json=JsonUtils.get_json_feature_extract_model(), headers=JsonUtils.header)
    assert response.json()['message'] == 'success'
    assert response.status_code == 200
    
def test_feature_extract_url():
    link_image = "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"
    response = client.post("/cosmenet/scanproduct/v2/onnx", json={"fullPath": link_image}, headers=JsonUtils.header)
    assert response.json()['message'] == 'success'
    assert response.status_code == 200

def test_feature_extract_unauthorized():
    response = client.post("/cosmenet/scanproduct/v2/onnx", json=JsonUtils.get_json_feature_extract_model())
    assert response.json()['detail'] == "Bearer token missing or unknown"
    assert response.status_code == 401

if __name__ == "__main__":
    test_feature_extract_success()
    test_feature_extract_unauthorized()