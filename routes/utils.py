from PIL import Image, UnidentifiedImageError
from io import BytesIO
import os, requests
from configs.logger import logger
from fastapi import HTTPException
from urllib.parse import urlparse

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def is_image_link(link_path):
    try:
        response = requests.get(link_path, stream=True)
        if response.status_code != 200:
            logger.error(f'image_path: {link_path}')
            raise HTTPException(status_code=404, detail="Link not found.")
        img = Image.open(BytesIO(response.content)).convert('RGB')
        logger.info(f'received image link: {link_path}')
        return img
    except UnidentifiedImageError as unidentified_image_error:
        logger.error(unidentified_image_error)
        logger.error(f'link ({link_path}) might not be an image')
        raise HTTPException(status_code=404, detail="Image Link is not valid.") from unidentified_image_error
        
def receive_image(link_path):
    try:
        if is_valid_url(link_path):
            img = is_image_link(link_path)
        elif not os.path.exists(link_path):
            logger.error(f'image_path: {link_path}')
            raise HTTPException(status_code=404, detail="Image Not Found.")
        else:
            logger.info(f'computing image path: {link_path}')
            img = Image.open(link_path).convert('RGB')
        return img
    except HTTPException as http_exception:
        logger.error(http_exception.detail)
        raise http_exception