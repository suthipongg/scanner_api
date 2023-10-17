from typing import Union

from fastapi import FastAPI, HTTPException
import uvicorn
from datetime import datetime
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from config import ConFig

app = FastAPI()

# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%d-%m-%Y")

if not os.path.exists('Logs'):
    try:
        os.mkdir('Logs')
    except Exception as err:
        logging.error(err)


def configure_logging():
    # register root logging
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler = TimedRotatingFileHandler('Logs/' + dt_string + '.log', when="midnight", interval=1, encoding='utf8')
    handler.suffix = "%d-%m-%Y"
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

if ConFig.LOGGING:
    configure_logging()

if ConFig.IS_ONNX_MODEL:
    from api.scanproduct_onnx_v3 import scanproduct_onnx_v3_api
    app.include_router(scanproduct_onnx_v3_api)

@app.get('/')
def index():
    return {'message': 'start'}

if __name__ == "__main__":
    uvicorn.run("app:app", 
                host=ConFig.HOST, 
                port=ConFig.PORT, 
                log_level="info", 
                reload=True)