from utils.env_loader import env, str2list
from utils.base_models import FullPathModel
from fastapi import APIRouter, File, UploadFile, Request, HTTPException
from controllers.image_processing import process_image, extract_image
import logging, sys, os
from pathlib import Path

router = APIRouter()

ALLOW_FILE = str2list(env["ALLOWED_EXTENSIONS"], sep=",")

def allowed_file(filename):
    return str(Path(filename).suffix).lower() in ALLOW_FILE

def save_file(file):
    contents = file.read()
    with open(Path(env['PATH_DIRECTORY_LOCAL_UAT']) / file.filename, "wb") as f:
        f.write(contents)
        logging.info(f" Files {file.filename} : saved to {Path(env['PATH_DIRECTORY_LOCAL_UAT']) / file.filename}") 

@router.post("/cosmenet/scanproduct/upload-files", tags=['scan_product'])
async def upload_image(request: Request, file: UploadFile = File(...)):
    try:
        if not allowed_file(file.filename):
            logging.info(f'File "{file.filename}" type is not allowed')    # LOG
            raise HTTPException(
                    status_code=400, 
                    detail=f'file type not allowed'
                )
    
        results = process_image(file.file)
        await save_file(file)
        logging.info(f' Files {file.filename} : successfully scanned') 

        return {
            'message': 'Files successfully scanned',
            'file': results
            }
        
    except HTTPException as e:
        raise HTTPException(status_code=400, detail=e.detail)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


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