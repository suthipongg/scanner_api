from models.extract_model import ExtractModel
from fastapi import APIRouter, HTTPException, Depends, status
from configs.security import UnauthorizedMessage, get_token
from configs.logger import logger
from controllers.feature_extract import feature_extractor
from routes.utils import receive_image

import sys, os

extract_route = APIRouter()

@extract_route.post(
    "/cosmenet/scanproduct/v2/onnx", 
    tags=['scan_product'],
    responses={status.HTTP_401_UNAUTHORIZED: dict(model=UnauthorizedMessage)},
    status_code=status.HTTP_200_OK
    )
async def extract_feature(
    body:ExtractModel,
    token_auth: str = Depends(get_token)
    ):
    try:
        body = body.model_dump()
        img = receive_image(body['image_path'])
        features = feature_extractor.extract(img)
        return {
            "message": "success",
            "embedded_feature": features,
        }
    except HTTPException as http_exception:
        logger.error(http_exception.detail)
        raise http_exception
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(f'file_name:{fname} - error_line:{exc_tb.tb_lineno} - error_type:{exc_type}')
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error") from e