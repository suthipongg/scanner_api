from datetime import datetime
import os, logging
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger('uvicorn')
logger.setLevel(logging.getLevelName(logging.INFO))

# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%Y-%m-%d")

if not os.path.exists('Logs'):
    try:
        os.mkdir('Logs')
    except Exception as err:
        logging.error(err)

def configure_logging():
    # register root logging
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - module:%(module)s - log_line:%(lineno)d - %(message)s")
    handler = TimedRotatingFileHandler('Logs/' + dt_string + '.log', when="midnight", interval=1, encoding='utf8')
    handler.suffix = "%Y-%m-%d"
    handler.setFormatter(formatter)
    logger.addHandler(handler)