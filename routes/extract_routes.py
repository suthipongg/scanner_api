from models.extract_model import ExtractModel
from fastapi import APIRouter, HTTPException, Depends, status
from configs.security import UnauthorizedMessage, get_token
from configs.logger import logger
from controllers.feature_extract import feature_extractor
from routes.utils import IMAGE_FORMATS

import sys, os, validators, requests
from PIL import Image

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
        if validators.url(body['image_path']):
            response = requests.get(body['image_path'], stream=True)
            if response.headers["Content-type"] not in IMAGE_FORMATS:
                logger.error(f'image_path: {body["image_path"]}')
                raise HTTPException(status_code=404, detail="Link image not in image format.")
            else:
                logger.info(f'computing image link: {body["image_path"]}')
                img = Image.open(response.raw).convert('RGB')
        elif not os.path.exists(body['image_path']):
            logger.error(f'image_path: {body["image_path"]}')
            raise HTTPException(status_code=404, detail="Image Not Found.")
        else:
            logger.info(f'computing image path: {body["image_path"]}')
            img = Image.open(body['image_path']).convert('RGB')
            
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