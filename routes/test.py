from fastapi import APIRouter
router = APIRouter()

@router.get('/test_get', tags=['test'])
async def index():
    return {
        'message': 'api start'
        }


from typing import List
from fastapi import Request, UploadFile, File
from fastapi import UploadFile

@router.post("/test_post", tags=['test'])
async def create_upload_files(request: Request, files: List[UploadFile] = File(...)):
    for file in files:
        contents = await file.read()

    return {
        'message': 'Files successfully scanned',
        'file': file.filename
        }

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse

@router.get('/test_show', tags=['test'])
def home(request: Request):
    return FileResponse("/home/music/Desktop/scanner_api/uploads/102_5.jpeg")

router.mount("/uploads", StaticFiles(directory="/home/music/Desktop/scanner_api/uploads"), name='uploads')
templates = Jinja2Templates(directory="templates")

@router.get('/test_show_front', tags=['test'], response_class=HTMLResponse)
def home(request: Request):
    return """
    <html>
        <head>
            <title></title>
        </head>
        <body>
        <img src="/uploads/102_5.jpeg">
        <h1>Hello World</h1>
        </body>
    </html>
    """
    
router.mount("/uploads", StaticFiles(directory="uploads"), name='uploads')
 
@router.get("/t", response_class=HTMLResponse)
def serve():
    return """
    <html>
        <head>
            <title></title>
        </head>
        <body>
        <img src="uploads/102_5.jpeg">
        <h1>Hello World</h1>
        </body>
    </html>
    """