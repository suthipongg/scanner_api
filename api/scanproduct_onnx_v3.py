from PIL import Image
import sys, os, logging
from pathlib import Path

from api.feature_extractor_onnx import FeatureExtractor

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


env = os.environ
LOG = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

scanproduct_onnx_v3_api = APIRouter()
fe = FeatureExtractor()

class ImgPath(BaseModel):
    message: str
    fullPath: str


def allowed_file(filename):
    return str(Path(filename).suffix).lower() in env["ALLOWED_EXTENSIONS"].split(",")

def extract_feature(img):
    try:
        return fe.extract(img)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        LOG.error(f"{str(e)} at {fname}")    # LOG
        raise HTTPException(
            status_code=500, 
            detail=str(e)
            )


@scanproduct_onnx_v3_api.post('/cosmenet/scanproduct/backend/v3/onnx', tags=['ScanProduct'])
def getfullpath(img_path: ImgPath):
    local_fullPath = img_path.fullPath
    LOG.info(f'local_fullPath : {local_fullPath}' )    # LOG
    
    if not os.path.exists(local_fullPath):
        LOG.info('No file part')    # LOG
        raise HTTPException(
            status_code=400, 
            detail=f"Can not find '{local_fullPath}' path"
            )
    
    elif allowed_file(local_fullPath):
        img = Image.open(local_fullPath)
        embedded_feature = extract_feature(img)
        LOG.info('Files successfully scanned')    # LOG
        return {
            'message': 'Files successfully scanned',
            'embedded_feature': embedded_feature,
            }
    
    else:
        LOG.info('File type is not allowed')    # LOG
        raise HTTPException(
            status_code=400, 
            detail=f'{local_fullPath} : File type is not allowed'
            )