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
    assert response.status_code == 200
    assert response.json()['message'] == 'success'

def test_feature_extract_unauthorized():
    response = client.post("/cosmenet/scanproduct/v2/onnx", json=JsonUtils.get_json_feature_extract_model())
    assert response.status_code == 401
    assert response.json()['detail'] == "Bearer token missing or unknown"

if __name__ == "__main__":
    test_feature_extract_success()
    test_feature_extract_unauthorized()