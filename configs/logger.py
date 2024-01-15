from datetime import datetime
import os, logging
from logging.handlers import TimedRotatingFileHandler

# Disable uvicorn access logger
uvicorn_access = logging.getLogger("uvicorn.access")
uvicorn_access.disabled = False

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.getLevelName(logging.DEBUG))

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