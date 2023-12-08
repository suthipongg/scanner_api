import sys, os, logging
from PIL import Image
from dotenv import load_dotenv
load_dotenv()

from fastapi import APIRouter, HTTPException, Request, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
# from api.feature_extractor import FeatureExtractor
import numpy as np
from typing import List
from controllers.scanproduct_v3 import extract_feature
from controllers.elasticsearch_query import ES_access
from script.func_query_body import query_cosine

env = os.environ
LOG = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

es_access = ES_access(env["ES_INDEX"], url=env["ES_URL"])

# fe = FeatureExtractor()
IMAGEDIR = "uploads/"

ReceiveImg = APIRouter()
ReceiveImg.mount("/uploads", StaticFiles(directory="uploads"), name='uploads')

templates = Jinja2Templates(directory="templates")
 
@ReceiveImg.get('/test', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
 
@ReceiveImg.post("/cosmenet/scanproduct/upload-files")
async def create_upload_files(request: Request, files: List[UploadFile] = File(...)):
    for file in files:
        contents = await file.read()
        #save the file
        with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
            f.write(contents)

    img = Image.open(f"{IMAGEDIR}{file.filename}").convert('RGB')
    embedded_feature = extract_feature(img)
    res = es_access.es.search(index=env["ES_INDEX"], body=query_cosine(embedded_feature, top_n=5, tag_name_compare=["train_split", "test_val"]))
    
    LOG.info('Files successfully scanned')    # LOG
    return {
        'message': 'Files successfully scanned',
        'res': res['hits']['hits'],
        }
    # return templates.TemplateResponse("index.html", {"request": request, "show": show})