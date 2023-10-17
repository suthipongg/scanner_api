from fastapi import APIRouter
from pydantic import BaseModel

from PIL import Image
import sys, os, logging
from pathlib import Path

from api.feature_extractor_onnx import FeatureExtractor
from config import ConFig

class FullPath(BaseModel):
    fullPath: str

LOG = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

scanproduct_onnx_v3_api = APIRouter()
fe = FeatureExtractor()

def allowed_file(filename):
    return str(Path(filename).suffix).lower() in ConFig.ALLOWED_EXTENSIONS

@scanproduct_onnx_v3_api.post('/cosmenet/scanproduct/test')
def index():
    LOG.info('test successfully')    # LOG
    return {'message': 'successfully'}

@scanproduct_onnx_v3_api.post('/cosmenet/scanproduct/backend/v3/onnx')
def getfullpath(local_path: FullPath):
    try:
        # local_fullPath = os.path.join(ConFig.PATH_DIRECTORY_LOCAL_UAT, os.path.join(*fullPath.split('/')[3:]))
        local_fullPath = local_path.fullPath
        LOG.info(f'local_fullPath : {local_fullPath}' )    # LOG
        
        if not os.path.exists(local_fullPath):
            LOG.info('No file part in Directory')    # LOG
            resp = {'message': 'No file part in Directory'}
            return resp, 200
        
        elif allowed_file(local_fullPath):
            img = Image.open(local_fullPath)
            embedded_feature = fe.extract(img).tolist()
            LOG.info('Files successfully scanned')    # LOG
            resp = {'message': 'Files successfully scanned',
                    'embedded_feature': embedded_feature,
                    }
            return resp, 200
        
        else:
            LOG.info('File type is not allowed')    # LOG
            resp = {local_fullPath: 'File type is not allowed'}
            return resp, 200


    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, e, fname, exc_tb.tb_lineno)
        LOG.info('Path is not correct')    # LOG
        resp = {'message': 'Path is not correct'}
        return resp, 200