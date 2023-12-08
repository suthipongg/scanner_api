from flask import Blueprint, jsonify, request
import os
from PIL import Image, ImageOps
from pyzbar.pyzbar import decode
from config import ConFig
import logging

LOG = logging.getLogger(__name__)

arg = ConFig()
scanbarcode_api = Blueprint('scanbarcode_api', __name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in arg.ALLOWED_EXTENSIONS


def BarcodeReader(image):
    decode_info = []
    try:
        # Decode the barcode image
        detectedBarcodes = decode(image)

        # If not detected then print the message
        if not detectedBarcodes:
            print("Barcode Not Detected or your barcode is blank/corrupted!")
            return None
        else:
            # Traverse through all the detected barcodes in image
            for barcode in detectedBarcodes:
                if barcode.data != "":
                    decode_result = barcode.data.decode('utf-8')
                    decode_info.append({"decode_result":str(decode_result), "type":barcode.type})
                else:
                    None
            return decode_info

    except Exception:
        return None



@scanbarcode_api.route('/cosmenet/scanbarcode/test', methods=["GET", "POST"])
def index():
    LOG.info('test successfully')    # LOG
    print('test successfully')
    return jsonify({'message': 'successfully'})



@scanbarcode_api.route('/cosmenet/scanbarcode/v2', methods=["POST"])
def scanbarcode():
    if request.method == "POST":    # Check method 
        re = request.get_json() # Read Json files
        fullPath = re['fullPath']   # Query param 'fullPath'   
        print(f'fullPath : {fullPath}')
        LOG.info(f'fullPath : {fullPath}' )    # LOG
        
        try:
            local_fullPath = os.path.join(arg.PATH_DIRECTORY_LOCAL, os.path.join(*fullPath.split('/')[3:]))
            LOG.info(f'local_fullPath : {local_fullPath}' )    # LOG
            if os.path.exists(local_fullPath):
                errors = {}
                success = False
            
                if allowed_file(fullPath):  # Check image not None and file
                    print(local_fullPath)
                    img = Image.open(local_fullPath)   # Image Loader
                    img = ImageOps.exif_transpose(img)
                    img = img.convert('RGB')    # Make sure img is color RGB
                    decode_info = BarcodeReader(img)    # Decode barcode
                    success = True
                else:
                    LOG.info('File type is not allowed')    # LOG
                    errors[fullPath] = 'File type is not allowed'
                
                if success and errors:
                    LOG.info('File(s) successfully scanned')    # LOG
                    errors['message'] = 'File(s) successfully scanned'
                    print('File(s) successfully scanned')
                    resp = jsonify(errors)
                    # resp.status_code = 500
                    return resp

                if success:
                    LOG.info('Files successfully scanned')    # LOG
                    print('Files successfully scanned')
                    resp = jsonify({'message': 'Files successfully scanned', 'decode_info':decode_info})
                    resp.status_code = 201
                    return resp
                else:
                    print(errors)
                    resp = jsonify(errors)
                    # resp.status_code = 500
                    return resp
            else:
                LOG.info('No file part in Directory')    # LOG
                print('No file part in Directory')
                resp = jsonify({'message': 'No file part in Directory'})
                # resp.status_code = 500
                return resp

        except:
            LOG.info('Path is not correct')    # LOG
            print('Path is not correct')
            resp = jsonify({'message': 'Path is not correct'})
            # resp.status_code = 500
            return resp

# path get form black end
@scanbarcode_api.route('/cosmenet/scanbarcode/backend', methods=["POST"])
def scanbarcode_backend():
    if request.method == "POST":    # Check method 
        re = request.get_json() # Read Json files
        fullPath = re['fullPath']   # Query param 'fullPath'   
        print(f'fullPath : {fullPath}')
        LOG.info(f'fullPath : {fullPath}' )    # LOG
        
        try:
            local_fullPath = os.path.join(arg.PATH_DIRECTORY_LOCAL_UAT, os.path.join(*fullPath.split('/')[3:]))
            LOG.info(f'local_fullPath : {local_fullPath}' )    # LOG
            if os.path.exists(local_fullPath):
                errors = {}
                success = False
            
                if allowed_file(fullPath):  # Check image not None and file
                    print(local_fullPath)
                    img = Image.open(local_fullPath)   # Image Loader
                    img = ImageOps.exif_transpose(img)
                    img = img.convert('RGB')    # Make sure img is color RGB
                    decode_info = BarcodeReader(img)    # Decode barcode
                    success = True
                else:
                    LOG.info('File type is not allowed')    # LOG
                    print('File type is not allowed')
                    errors[fullPath] = 'File type is not allowed'
                
                if success and errors:
                    LOG.info('File(s) successfully scanned')    # LOG
                    print('File(s) successfully scanned')
                    errors['message'] = 'File(s) successfully scanned'
                    resp = jsonify(errors)
                    # resp.status_code = 500
                    return resp

                if success:
                    LOG.info('Files successfully scanned')    # LOG
                    print('Files successfully scanned')
                    resp = jsonify({'message': 'Files successfully scanned', 'decode_info':decode_info})
                    resp.status_code = 201
                    return resp
                else:
                    print(errors)
                    resp = jsonify(errors)
                    # resp.status_code = 500
                    return resp
            else:
                LOG.info('No file part in Directory')    # LOG
                print('No file part in Directory')
                resp = jsonify({'message': 'No file part in Directory'})
                # resp.status_code = 500
                return resp

        except:
            LOG.info('Path is not correct')    # LOG
            print('Path is not correct')
            resp = jsonify({'message': 'Path is not correct'})
            # resp.status_code = 500
            return resp