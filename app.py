from fastapi import FastAPI
import uvicorn

from datetime import datetime
import os, logging
from logging.handlers import TimedRotatingFileHandler
from dotenv import load_dotenv
load_dotenv()

env = os.environ
app = FastAPI(title=env["TITLE"])

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

if int(env["LOGGING"]):
    configure_logging()

if int(env["IS_ONNX_MODEL"]):
    from api.scanproduct_onnx_v3 import scanproduct_onnx_v3_api
    app.include_router(scanproduct_onnx_v3_api)

@app.get('/', tags=['Root'])
def index():
    return {
        'message': 'api start'
        }


if __name__ == "__main__":
    uvicorn.run("app:app", 
                host=env["HOST"], 
                port=int(env["PORT"]), 
                log_level="info", 
                reload=True
                )