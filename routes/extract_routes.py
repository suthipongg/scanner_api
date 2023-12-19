from models.fullpath_model import FullPathModel
from fastapi import APIRouter, HTTPException
from controllers.feature_extract import extract_image
import sys, os

router = APIRouter()

@router.post("/cosmenet/scanproduct/v2/onnx", tags=['scan_product'])
async def extract_feature(body:FullPathModel):
    try:
        features = extract_image(body.fullPath)
        return {
            "message": "success",
            "embedded_feature": features,
        }
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error") from e