from flask import Blueprint, request, jsonify, json
from PIL import Image
import sys, os, logging
from pathlib import Path

from api.feature_extractor_onnx import FeatureExtractor
from config import ConFig


LOG = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

scanproduct_onnx_v3_api = Blueprint('scanproduct_onnx_api', __name__)
fe = FeatureExtractor()


def allowed_file(filename):
    return str(Path(filename).suffix).lower() in ConFig.ALLOWED_EXTENSIONS


@scanproduct_onnx_v3_api.route('/cosmenet/scanproduct/test', methods=["GET", "POST"])
def index():
    LOG.info('test successfully')    # LOG
    return jsonify({'message': 'successfully'})

@scanproduct_onnx_v3_api.route('/cosmenet/scanproduct/backend/v3/onnx', methods=["POST", "GET"])
def getfullpath():
    try:
        if request.method == "POST":
            re = request.get_json()
            fullPath = re["fullPath"]
            LOG.info(f'fullPath : {fullPath}' )    # LOG
            
        elif request.method == "GET":
            LOG.info('method GET api scan product')    # LOG
            return jsonify({'message': 'method GET api scan product'})
    
        local_fullPath = os.path.join(ConFig.PATH_DIRECTORY_LOCAL_UAT, os.path.join(*fullPath.split('/')[3:]))
        local_fullPath = fullPath
        LOG.info(f'local_fullPath : {local_fullPath}' )    # LOG
        
        if os.path.exists(local_fullPath):
            if allowed_file(fullPath):
                img = Image.open(local_fullPath)
                embedded_feature = fe.extract(img).tolist()
                LOG.info('Files successfully scanned')    # LOG
                resp = json.dumps({'message': 'Files successfully scanned',
                                    'embedded_feature': embedded_feature,
                                    })
                return resp, 200
            else:
                LOG.info('File type is not allowed')    # LOG
                resp = jsonify({fullPath: 'File type is not allowed'})
                return resp, 200
        
        else:
            LOG.info('No file part in Directory')    # LOG
            resp = jsonify({'message': 'No file part in Directory'})
            return resp, 200

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, e, fname, exc_tb.tb_lineno)
        LOG.info('Path is not correct')    # LOG
        resp = jsonify({'message': 'Path is not correct'})
        return resp, 200