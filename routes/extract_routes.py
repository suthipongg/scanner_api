from fastapi import APIRouter, Depends, status
from configs.security import UnauthorizedMessage, get_token
from configs.logger import logger
from controllers.feature_extract import feature_extractor
from routes.utils import receive_image
from models.extract_model import ExtractModel
from utils.exception_handling import handle_exceptions
from PIL import Image

extract_route = APIRouter(tags=['scan_product'])

@extract_route.post(
    "/cosmenet/scanproduct/v2/onnx", 
    responses={status.HTTP_401_UNAUTHORIZED: dict(model=UnauthorizedMessage)},
    status_code=status.HTTP_200_OK
    )
@handle_exceptions
async def extract_feature(
    body:ExtractModel,
    token_auth: str = Depends(get_token)
    ):
    body = body.model_dump()
    img = receive_image(body['image_path'])
    features = feature_extractor.extract(img)
    logger.info('Extracted features successfully')
    return {
        "message": "success",
        "embedded_feature": features,
    }
    
@extract_route.get(
    "/cosmenet/scanproduct/v2/onnx/warmup", 
    responses={status.HTTP_401_UNAUTHORIZED: dict(model=UnauthorizedMessage)},
    status_code=status.HTTP_200_OK
    )
@handle_exceptions
async def extract_feature(
    token_auth: str = Depends(get_token)
    ):
    logger.info('Warming up the model')
    dummy_img = Image.new('RGB', size=(224, 224))
    feature_extractor.extract(dummy_img)
    logger.info('Warmup success')
    return {
        "message": "warmup success"
    }